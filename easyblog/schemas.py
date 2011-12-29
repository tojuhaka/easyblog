from formencode import Schema, validators

class SignUpSchema(Schema):
    filter_extra_fields = True
    allow_extra_fields = True

    username = validators.MinLength(5, not_empty=True)
    password = validators.MinLength(6, not_empty=True)
    password_confirm = validators.MinLength(6, not_empty=True)

    #TODO: other than chained_validators
    chained_validators = [validators.FieldsMatch('password', 'password_confirm')]
    email = validators.MinLength(4, not_empty=True)
