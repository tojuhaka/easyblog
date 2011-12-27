from passlib.context import CryptContext
from pyramid.view import view_config
from pyramid.security import Allow, Everyone

USERS = {'editor':'editor',
          'viewer':'viewer'}
GROUPS = {'editor':['group:editors']}


acl = [ (Allow, Everyone, 'view'),
        (Allow, 'group:editors', 'edit') ]
# Salt for pasword hashes
salt = 'torpedo'
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

@view_config(context='easyblog.models.Main')
def users(context):
    return context['users']

def groupfinder(userid, request):
    if userid in users:
        return GROUPS.get(userid, [])

