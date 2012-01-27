from passlib.context import CryptContext
from pyramid.security import Allow, Everyone
from pyramid.httpexceptions import HTTPForbidden
from pyramid.events import NewRequest, subscriber
from easyblog.utilities import get_tool


# TODO: HIDE?
acl = [(Allow, Everyone, 'view'),
        (Allow, 'group:members', 'edit'),
        (Allow, 'group:admins', 'edit_all'),
        (Allow, 'group:admins', 'edit'),
        (Allow, 'group:admins', 'create_blog'),
        (Allow, 'group:editors', 'create_blog')]

# Salt for pasword hashes, move to database or somewhere safe (and change it )
salt = u'torpedo'

# Crypt config for password hashes
pwd_context = CryptContext(
    #replace this list with the hash(es) you wish to support.
    #this example sets pbkdf2_sha256 as the default,
    #with support for legacy des_crypt hashes.
    schemes=["pbkdf2_sha256", "des_crypt"],
    default="pbkdf2_sha256",

    #vary rounds parameter randomly when creating new hashes...
    all__vary_rounds="10%",

    #set the number of rounds that should be used...
    #(appropriate values may vary for different schemes,
    # and the amount of time you wish it to take)
    pbkdf2_sha256__default_rounds=8000,
    )




def groupfinder(userid, request):
    if userid in get_tool('users', request):
        return get_tool('groups', request)[userid]

#Protect sessions from Cross-site request forgery attacks
@subscriber(NewRequest)
def csrf_validation(event):
    if event.request.method == "POST":
        token = event.request.POST.get("_csrf")
        if token is None or token != event.request.session.get_csrf_token():
            raise HTTPForbidden("CSRF token is missing or invalid")
