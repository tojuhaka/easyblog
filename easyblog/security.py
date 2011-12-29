from passlib.context import CryptContext
from pyramid.security import Allow, Everyone
from pyramid_zodbconn import get_connection

# TODO: make GUI for groups
acl = [ (Allow, Everyone, 'view'),
        (Allow, 'group:members', 'edit'),
        (Allow, 'group:admins', 'edit_all'),
       (Allow, 'group:admins', 'edit')]

# Salt for pasword hashes, move to database or somewhere safe (and change it )
salt = u'torpedo'
# Crypt config for password hashes
pwd_context = CryptContext(
    #replace this list with the hash(es) you wish to support.
    #this example sets pbkdf2_sha256 as the default,
    #with support for legacy des_crypt hashes.
    schemes=["pbkdf2_sha256", "des_crypt" ],
    default="pbkdf2_sha256",

    #vary rounds parameter randomly when creating new hashes...
    all__vary_rounds = "10%",

    #set the number of rounds that should be used...
    #(appropriate values may vary for different schemes,
    # and the amount of time you wish it to take)
    pbkdf2_sha256__default_rounds = 8000,
    )

# TODO: BETTER SOLUTION

def groupfinder(userid, request):
    context = get_connection(request).root()['app_root']
    if userid in context['users']:
        return context['groups'].get(userid, [])

