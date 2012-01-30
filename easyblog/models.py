from persistent.mapping import PersistentMapping
from persistent import Persistent

from easyblog.security import pwd_context, salt, acl, group_names

from datetime import datetime
from pyramid.security import Allow

from easyblog.interfaces import IComment
from zope.interface import implements

# Main root object in our ZODB database
class Main(PersistentMapping):
    """ Root object for ZODB """
    __name__ = None
    __parent__ = None
    __acl__ = acl

class Users(PersistentMapping):
    """ Contains all the users """

    def _generate_id(self):
        return len(self.keys()) + 1

    def has_user(self, username):
        if username in self.keys():
            return True
        return False

    def add(self, username, password, email):
        user = User(username, password, email, self._generate_id())
        user.__name__ = username
        user.__parent__ = self
        self[user.username] = user


class User(Persistent):
    @property
    def __acl__(self):
        acls = [(Allow, 'u:%s' % self.username, 'edit_user'),
                (Allow, group_names['admin'], 'edit_user')]
        return acls

    def __init__(self, username, password, email, id):
        self.username = username
        self.password = pwd_context.encrypt(password + salt)
        self.id = id
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

    def remove(self, username, group):
        if group in self[username]:
            self[username].remove(group)

    def flush(self, username):
        self[username] = []
    
    def add_policy(self, policy):
        """ Updates the group-policy with dict that contains
        usernames and list of groups behind it """
        for username in policy.keys():
            self[username] = policy[username] + [u'u:%s' % username]


class Blogs(PersistentMapping):
    """ Blog mapper which contains all the logs """

    def __init__(self):
        super(PersistentMapping, self).__init__()

        # Use running number as id for blog
        self.blog_number = 0

    def add(self, name, username):
        blog = Blog(name, username, u'b%i' % self.blog_number)
        self[blog.id] = blog
        self.blog_number += 1
        blog.__parent__ = self
        blog.__name__ = blog.id

    def has_blog(self, name):
        for key in self.keys():
            if self[key].name == name:
                return True
        return False


# Page for single blog
class Blog(PersistentMapping):
    implements(IComment)
    @property
    def __acl__(self):
        acls = [(Allow, 'u:%s' % o, 'edit_blog') for o in self.owners]
        #TODO: remove admin
        acls.append((Allow, group_names['admin'], 'edit_blog'))
        return acls

    def __init__(self, name, username, id):
        super(PersistentMapping, self).__init__()
        self.name = name
        self.owners = [username, 'admin']
        self.comments = "HERE IS SOME COMMENTS"
        # Convert name for path. This is also the id of the page.
        # TODO: Check encode
        self.id = id
        

    def add(self, subject, text, username):
        post = BlogPost(subject, text, username)
        self[post.id] = post
        post.__name__ = id
        post.__parent__ = self


# Single post. Blog page contains multiple Blog posts.
class BlogPost(Persistent):
    def __init__(self, subject, text, username):
        self.username = username
        self.subject = subject
        self.text = text
        self.timestamp = datetime.now()

        # Create md5 hash from username and timestamp
        # to act as id for the BlogPost
        import hashlib
        m = hashlib.md5()
        m.update(username)
        m.update(self.timestamp.isoformat())
        self.id = m.digest()

    def time(self):
        return "%s %s" % (self.timestamp.strftime("%x"),
        self.timestamp.strftime("%X"))

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Main()
        users = Users()
        blogs = Blogs()
        groups = Groups()
        app_root['users'] = users
        app_root['blogs'] = blogs
        app_root['groups'] = groups

        users.__parent__ = app_root
        users.__name__ = 'users'
        blogs.__name__ = 'blogs'
        blogs.__parent__ = app_root
        groups.__parent__ = app_root

        users.add('admin', 'adminpw#', 'admin@admin.com')
        groups.add('admin', group_names['admin'])

        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
