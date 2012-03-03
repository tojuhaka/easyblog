from persistent.mapping import PersistentMapping
from persistent import Persistent

from easyblog.security import pwd_context, salt, acl, group_names

from datetime import datetime
from pyramid.security import Allow

from easyblog.interfaces import ISiteRoot, IComment, IContainer, IContent, IPage
from easyblog.interfaces import IAbout, IContact, IBlogs, INews, INavPage
from zope.interface import implements

from .utilities import order

class Container(PersistentMapping):
    """ Base container for all the objects
    that store other objects for example
    Blogs and News are containers """
    implements(IContainer)

    def __init__(self, crumb_name, owner, id):
        PersistentMapping.__init__(self)
        self.item_number = 0
        self.timestamp = datetime.now()
        self.id = id
        self.owner = owner

        # Name used in breadcrumps
        self.crumb_name = crumb_name

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

    def date(self):
        return u"%s" % (self.timestamp.strftime("%x"))
        
class Content(Persistent):
    implements(IContent)
    """ Base content for all the objects
    that are defined as contents for example
    single blogpost or single news item is
    a content """
    def __init__(self, crumb_name, owner, id):
        Persistent.__init__(self)
        self.owner = owner
        self.timestamp = datetime.now()
        self.id = id

        # Name used in breadcrumps
        self.crumb_name = crumb_name

    def date(self):
        return u"%s" % (self.timestamp.strftime("%x"))

# Main root object in our ZODB database
class Main(PersistentMapping):
    implements(IPage, ISiteRoot)
    """ Root object for ZODB """
    __name__ = None
    __parent__ = None
    __acl__ = acl

class Page(Content):
    implements(IPage)
    """ Editable static page """
    #TODO: 'Pages' container, make the container - content
    # relationship more modular
    @property
    def __acl__(self):
        acls = [(Allow, group_names['editor'], 'edit_content')]
        return acls

    def __init__(self, title, text, owner, id):
        Content.__init__(self, title, owner, id)
        self.title = title
        self.text = text

class AboutPage(Page):
    implements(IAbout, IPage, INavPage)
    
class ContactPage(Page):
    implements(IContact, INavPage)

class Groups(Container):
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

class Users(Container):
    implements(IPage)
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
        self.item_number += 1


class User(Content):
    implements(IPage)
    @property
    def __acl__(self):
        acls = [(Allow, 'u:%s' % self.username, 'edit_content')]
        return acls

    def __init__(self, username, password, email):
        Content.__init__(self, username, username, username)
        self.username = username
        self.password = pwd_context.encrypt(password + salt)
        self.email = email

    def edit(self, password, email):
        self.password = pwd_context.encrypt(password + salt)
        self.email = email

    def validate_password(self, password):
        return pwd_context.verify(password + salt, self.password)




class Blogs(Container):
    """ Blog mapper which contains all the logs """
    implements(IPage, IBlogs)
    @property
    def __acl__(self):
        acls = [(Allow, group_names['editor'], 'edit_container')]
        return acls

    def add(self, name, description, image_url, owner):
        blog = Blog(name, description, image_url,
                owner, u'b%i' % self.item_number)
        self[blog.id] = blog
        blog.__parent__ = self
        blog.__name__ = blog.id
        self.item_number += 1
        return blog

    def has_blog(self, name):
        for key in self.keys():
            if self[key].name == name:
                return True
        return False

class Blog(Container):
    implements(IPage)
    """ Blog which contains posts from user """

    @property
    def __acl__(self):
        acls = [(Allow, 'u:%s' % self.owner, 'edit_content')]
        return acls

    def __init__(self, name, description, image_url, owner, id):
        Container.__init__(self, name, owner, id)
        self.name = name
        self.comments = ""
        self.image_url = image_url
        self.description = description

    def add(self, subject, text, username):
        post = BlogPost(subject, text, username, u'p%i' % self.item_number)
        self[post.id] = post
        post.__name__ = post.id
        post.__parent__ = self
        self.item_number += 1
        return post

class BlogPost(Content):
    """ Single post inside blog """
    implements(IPage, IComment)

    @property
    def __acl__(self):
        acls = [(Allow, 'u:%s' % self.owner, 'edit_content')]
        return acls

    def __init__(self, title, text, owner, id):
        Content.__init__(self, title, owner, id)
        self.title = title
        self.text = text
        self.comments = ""

    def time(self):
        return "%s %s" % (self.timestamp.strftime("%x"),
        self.timestamp.strftime("%X"))


class NewsItem(Content):
    """ Contains all the information about
    one news item """
    implements(IPage, IComment, IContent)

    @property
    def __acl__(self):
        acls = [(Allow, 'u:%s' % self.owner, 'edit_content'),
                (Allow, group_names['editor'], 'edit_content')]
        return acls

    def __init__(self, title, text, image_url, owner, id):
        Content.__init__(self, title, owner, id)
        # super(PersistentMapping, self).__init__()
        self.title = title
        self.text = text
        self.image_url = image_url
        self.comments = ""

    def date(self):
        return u"%s" % (self.timestamp.strftime("%x"))


class News(Container):
    """ Contains all the news items """
    implements(IPage, INews)
    @property
    def __acl__(self):
        acls = [(Allow, group_names['editor'], 'edit_container')]
        return acls

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

        # Create base containers 
        users = Users('users', 'main', 'users')
        blogs = Blogs('blogs', 'main', 'blogs')
        groups = Groups('groups', 'main', 'groups')
        news = News('news', 'main', 'news')

        app_root['users'] = users
        app_root['blogs'] = blogs
        app_root['groups'] = groups
        app_root['news'] = news

        # static pages
        about = AboutPage('about', 'content',  'main', 'about')
        contact = ContactPage('about', 'content',  'main', 'about')
        app_root['about'] = about
        app_root['contact'] = contact

        users.__parent__ = app_root
        users.__name__ = 'users'
        blogs.__name__ = 'blogs'
        blogs.__parent__ = app_root
        groups.__parent__ = app_root
        news.__name__ = 'news'
        news.__parent__ = app_root
        contact.__name__ = 'contact'
        contact.__parent__ = app_root
        about.__name__ = 'about'
        about.__parent__ = app_root

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
