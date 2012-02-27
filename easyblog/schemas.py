from formencode import Schema, validators, All
from formencode import FancyValidator, Invalid
from pyramid_zodbconn import get_connection

from easyblog.utilities import has_special

# Validate username
class UniqueUsername(FancyValidator):
    def _to_python(self,value,state):
        context = get_connection(state.request).root()['app_root']
        if value in context['users']:
            raise Invalid(
                'That username already exists.',
                value, state
            )
        return value

class UniqueEmail(FancyValidator):
    def _to_python(self,value,state):
        context = get_connection(state.request).root()['app_root']
        for user in context['users']:
            if context['users'][user].email == value:
                raise Invalid(
                    'That email already exists.',
                    value, state
                )
        return value

class RemoveSpecial(FancyValidator):
    def _to_python(self, value, state):
        if has_special(value) != None:
            raise Invalid('Invalid username. Remove special Characters', 
                            value, state)
        return value


class BaseSchema(Schema):
    filter_extra_fields = True
    allow_extra_fields = True

# Schema for signup form
class SignUpSchema(BaseSchema):
    username = All(validators.MinLength(4, not_empty=True), 
                    RemoveSpecial(), UniqueUsername())
    password = validators.MinLength(6, not_empty=True)
    password_confirm = validators.MinLength(6, not_empty=True)
    email = All(validators.Email(not_empty=True), UniqueEmail())
    chained_validators = [validators.FieldsMatch('password', 'password_confirm')]

class LoginSchema(BaseSchema):
    username = validators.MinLength(3, not_empty=False)

# Schema for user editform
class UserEditSchema(BaseSchema):
    email = All(validators.Email(not_empty=True), UniqueEmail())
    new_password = validators.MinLength(6, not_empty=False)
    new_password_confirm = validators.MinLength(6, not_empty=False)
    chained_validators = [validators.FieldsMatch('new_password', 'new_password_confirm')]

# Schema for users edit. Admin's view.
class UsersEditSchema(BaseSchema):
    search = validators.MinLength(1, not_empty=True)

# Schema for blogpage creation
class BlogCreateSchema(BaseSchema):
    blogname = validators.MinLength(6, not_empty=True)
    text = validators.MinLength(10, not_empty=True)
    image_url = validators.URL(add_http=False, check_exists=True)

class BlogPostSchema(BaseSchema):
    """ Schema for blogpost """
    title = validators.MinLength(3, not_empty=True)
    text = validators.MinLength(10, not_empty=True)

class PageEditSchema(BaseSchema):
    """ Schema for Page edit """
    title = validators.MinLength(3, not_empty=True)
    text = validators.MinLength(10, not_empty=True)

# Schema for adding post to blog
class NewsCreateSchema(BaseSchema):
    """ Schema for single news form """
    title = validators.MaxLength(60, not_empty=True)
    text = validators.MinLength(10, not_empty=True)
    image_url = validators.URL(add_http=False, check_exists=True)



