from persistent.mapping import PersistentMapping
from persistent import Persistent

from easyblog.security import pwd_context, salt, acl, group_names

from datetime import datetime
from pyramid.security import Allow

from easyblog.interfaces import ISiteRoot, IComment, IContainer, IContent
from zope.interface import implements

from .utilities import order

class Container(PersistentMapping):
    implements(IContainer)
    """ Base container for all the objects
    that store other objects for example
    Blogs and News are containers """
    def add(self):
        raise NotImplementedError("Add method not defined")

    def remove(self, id):
        return self.pop(id)

    def order_by_time(self):
        """ Return a list of contents ordered by time """
        ordered_keys = sorted(self.keys(),
            key=lambda item: self[item].timestamp, reverse=True)
        return order(self, ordered_keys)

    def items_by_owner(self, owner):
        """ Return list of all the items created by owner """
        return [item for item in self.keys() if owner == self[item].owner]
        
class Content(Persistent):
    """ Base content for all the objects
    that are defined as contents for example
    single blogpost or single news item is
    a content """
    pass

# Main root object in our ZODB database
class Main(PersistentMapping):
    implements(ISiteRoot)
    """ Root object for ZODB """
    __name__ = None
    __parent__ = None
    __acl__ = acl


class Users(PersistentMapping):
    """ Contains all the users """

    def has_user(self, username):
        if username in self.keys():
            return True
        return False

    def add(self, username, password, email):
        user = User(username, password, email)
        user.__name__ = username
        user.__parent__ = self
        self[user.username] = user


class User(Persistent):

    @property
    def __acl__(self):
        acls = [(Allow, 'u:%s' % self.username, 'edit_content')]
        return acls

    def __init__(self, username, password, email):
        self.username = username
        self.password = pwd_context.encrypt(password + salt)
        self.email = email

    def edit(self, password, email):
        self.password = pwd_context.encrypt(password + salt)
        self.email = email

    def validate_password(self, password):
        return pwd_context.verify(password + salt, self.password)


class Groups(PersistentMapping):
    """ Contains the information about the groups of
    the users """

    def add(self, username, group):
        """ Add a single group to username """
        try:
            self[username]
        except KeyError:
            self[username] = []

        if not group in self[username]:
            self[username] += [group]

    def remove_group(self, username, group):
        if group in self[username]:
            self[username].remove(group)

    def flush(self, username):
        self[username] = []

    def add_policy(self, policy):
        """ Updates the group-policy with dict that contains
        usernames and list of groups behind it. Add also the
        user-marker "u:user" to group. We need it for __acl__ inside class. """

        for username in policy.keys():
            self[username] = policy[username] + [u'u:%s' % username]


class Blogs(Container):
    """ Blog mapper which contains all the logs """

    def __init__(self):
        super(PersistentMapping, self).__init__()

        # Use running number as id for blog
        self.blog_number = 0

    def add(self, name, description, image_url, owner):
        blog = Blog(name, description, image_url,
                owner, u'b%i' % self.blog_number)
        self[blog.id] = blog
        blog.__parent__ = self
        blog.__name__ = blog.id
        self.blog_number += 1
        return blog

    def has_blog(self, name):
        for key in self.keys():
            if self[key].name == name:
                return True
        return False

class Blog(Container):
    """ Blog which contains posts from user """

    @property
    def __acl__(self):
        acls = [(Allow, 'u:%s' % self.owner, 'edit_content')]
        return acls

    def __init__(self, name, description, image_url, owner, id):
        super(PersistentMapping, self).__init__()
        self.post_number = 0
        self.name = name
        self.owner = owner
        self.comments = "HERE IS SOME COMMENTS"
        self.image_url = image_url
        self.description = description
        self.id = id

    def add(self, subject, text, username):
        post = BlogPost(subject, text, username, u'p%i' % self.post_number)
        self[post.id] = post
        post.__name__ = post.id
        post.__parent__ = self
        self.post_number += 1
        return post


class BlogPost(Persistent):
    """ Single post inside blog """
    implements(IComment, IContent)

    @property
    def __acl__(self):
        acls = [(Allow, 'u:%s' % self.owner, 'edit_content')]
        return acls

    def __init__(self, title, text, owner, id):
        self.owner = owner
        self.title = title
        self.text = text
        self.timestamp = datetime.now()
        self.comments = "COMMENTS FROM BLOGPOST"
        self.id = id

    def time(self):
        return "%s %s" % (self.timestamp.strftime("%x"),
        self.timestamp.strftime("%X"))


class NewsItem(Persistent):
    """ Contains all the information about
    one news item """
    implements(IComment, IContent)

    @property
    def __acl__(self):
        acls = [(Allow, 'u:%s' % self.owner, 'edit_content'),
                (Allow, group_names['editor'], 'edit_content')]
        return acls

    def __init__(self, title, text, image_url, username, id):
        # super(PersistentMapping, self).__init__()
        self.title = title
        self.text = text

        self.image_url = image_url
        self.owner = username
        self.id = id
        self.timestamp = datetime.now()
        self.comments = "COMMENTS FROM NEWSITEM"

    def date(self):
        return u"%s" % (self.timestamp.strftime("%x"))

    # def date_and_time(self):
    #     return u"%s %s" % (self.timestamp.strftime("%x"),
    #     self.timestamp.strftime("%X"))


class News(Container):
    """ Contains all the news items """

    def __init__(self):
        super(PersistentMapping, self).__init__()

        # Use running number as id for blog
        self.item_number = 0

    def add(self, title, text, image_url, owner):
        """ Add single news item and return it """
        item = NewsItem(title, text, image_url, owner,
                u'n%i' % self.item_number)
        self[item.id] = item
        self.item_number += 1
        item.__parent__ = self
        item.__name__ = item.id
        return item

    def has_item(self, title):
        for key in self.keys():
            if self[key].title == title:
                return True
        return False


def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Main()
        users = Users()
        blogs = Blogs()
        groups = Groups()
        news = News()
        app_root['users'] = users
        app_root['blogs'] = blogs
        app_root['groups'] = groups
        app_root['news'] = news

        users.__parent__ = app_root
        users.__name__ = 'users'
        blogs.__name__ = 'blogs'
        blogs.__parent__ = app_root
        groups.__parent__ = app_root
        news.__name__ = 'news'
        news.__parent__ = app_root

        users.add('admin', 'adminpw#', 'admin@admin.com')
        users.add('editor', 'editorpw#', 'editor@editor.com')
        groups.add('admin', group_names['admin'])
        groups.add('editor', group_names['editor'])
        # TODO: automate 'u:user' group so we don't have to
        # put it manually
        groups.add('editor', u'u:editor')

        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
