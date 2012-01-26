from persistent.mapping import PersistentMapping
from persistent import Persistent

from easyblog.security import pwd_context, salt, acl
from easyblog.config import admins_group

from datetime import datetime
from pyramid.security import Allow, Everyone


# Main root object in our ZODB database
class Main(PersistentMapping):
    __name__ = None
    __parent__ = None
    __acl__ = acl


# Contains all the users
class Users(PersistentMapping):
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


# Single user, TODO: passwords and other information
class User(Persistent):
    #TODO: DO IT!
    # @property
    # def __acl__(self):
    #     acls = [(Allow, 'u:%d' % o.id, 'edit') for o in self.owners]
    #     return acls

    def __init__(self, username, password, email, id):
        self.username = username
        self.password = pwd_context.encrypt(password + salt)
        self.id = id
        self.email = email
        self.owners = [username]
        #TODO: Timestamp, hash?

    def edit(self, password, email):
        self.password = pwd_context.encrypt(password + salt)
        self.email = email

    def validate_password(self, password):
        return pwd_context.verify(password + salt, self.password)


class Groups(PersistentMapping):
    def add(self, username, group):
        self[username] = group


# Blog mapper which cointains all the blogs
class Blogs(PersistentMapping):
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
    def __init__(self, name, username, id):
        super(PersistentMapping, self).__init__()
        self.name = name
        self.username = username
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


#TODO REMOVE
class Page(Persistent):
    def __init__(self, data):
        self.data = data


def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Main()
        users = Users()
        blogs = Blogs()
        groups = Groups()
        app_root['users'] = users
        app_root['blogs'] = blogs
        app_root['groups'] = groups

        #TODO: REMOVE
        frontpage = Page('this is the front page')
        frontpage.__name__ = 'FrontPage'
        frontpage.__parent__ = app_root
        app_root['FrontPage'] = frontpage

        users.__parent__ = app_root
        users.__name__ = 'users'
        blogs.__name__ = 'blogs'
        blogs.__parent__ = app_root
        groups.__parent__ = app_root

        users.add('admin', 'adminpw#', 'admin@admin.com')
        groups.add('admin', admins_group)

        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
