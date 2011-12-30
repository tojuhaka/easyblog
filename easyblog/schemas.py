from formencode import Schema, validators, All
from formencode import FancyValidator, Invalid
from pyramid_zodbconn import get_connection

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



class BaseSchema(Schema):
    filter_extra_fields = True
    allow_extra_fields = True

# Schema for signup form
class SignUpSchema(BaseSchema):
    username = All(validators.MinLength(4, not_empty=True), UniqueUsername())
    password = validators.MinLength(6, not_empty=True)
    password_confirm = validators.MinLength(6, not_empty=True)
    email = All(validators.Email(not_empty=True), UniqueEmail())
    chained_validators = [validators.FieldsMatch('password', 'password_confirm')]

class LoginSchema(BaseSchema):
    pass

class UserEditSchema(BaseSchema):
    pass

