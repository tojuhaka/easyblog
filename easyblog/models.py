from persistent.mapping import PersistentMapping
from persistent import Persistent


from easyblog.security import pwd_context, salt, acl
from easyblog.config import admins_group

import urllib

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
    def add(self, username, group):
        self[username] = group

# Blog mapper cointaingin all the blogs
class Blogs(PersistentMapping):
    def add(self, name, username):
        page = Blog(name, username)
        self[page.url_name] = page
        page.__name__ = name
        page.__parent__ = self

    def has_blog(self, name):
        url_name = urllib.quote(name)
        if url_name in self.keys():
            return True
        return False

# Page for single blog
class Blog(Persistent):
    def __init__(self,name, username):
        self.name = name
        self.username = username
        self.blogposts = []
        # Convert name for path. This is also the id of the page.
        self.url_name = urllib.quote(name)

# Single post. Blog page contains multiple Blog posts.
class BlogPost(Persistent):
    def __init__(self, subject, text, username):
        self.username = username
        self.subject = subject
        self.text = text

#TODO REMOVE
class Page(Persistent):
    def __init__(self,data):
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
        frontpage=Page('this is the front page')
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
