from persistent.mapping import PersistentMapping
from persistent import Persistent

from easyblog.exceptions import UsernameAlreadyInUseException 
from easyblog.exceptions import FieldsNotDefinedException

from easyblog.security import pwd_context, salt, acl

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
        return username in self.keys()

    def add(self, username, password):
        if self.has_user(username):
            raise UsernameAlreadyInUseException(username)
        if not username or not password:
            raise FieldsNotDefinedException()

        user = User(username, password, self._generate_id())
        self[user.username] = user

# Single user, TODO: passwords and other information
class User(Persistent):
    def __init__(self, username, password, id):
        self.username = username
        self.password = pwd_context.encrypt(password + salt)
        self.id = id

    def validate_password(self, password):
        return pwd_context.verify(password + salt, self.password)

class Groups(PersistentMapping):
    pass


# Blog mapper cointaingin all the blogs
class Blog(PersistentMapping):
        pass

# Page for single blog
class BlogPage(Persistent):
    def __init(self,name,user):
        self.name = name
        self.user = user
        self.blogposts = []

# Single post. Blog page contains multiple Blog posts.
class BlogPost(Persistent):
    def __init__(self, subject, text, user):
        self.user = user
        self.subject = subject
        self.text = text

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Main()
        users = Users()
        blog = Blog()
        app_root['users'] = users
        app_root['blog'] = blog

        users.__parent__ = app_root
        blog.__parent__ = app_root

        users.add('admin', 'adminpw#')

        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
