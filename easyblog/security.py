from passlib.context import CryptContext
from pyramid.security import Allow, Everyone
from pyramid_zodbconn import get_connection
from pyramid.security import authenticated_userid, has_permission
from pyramid.httpexceptions import HTTPForbidden
from pyramid.events import NewRequest, subscriber


# TODO: make GUI for groups
acl = [(Allow, Everyone, 'view'),
        (Allow, 'group:members', 'edit'),
        (Allow, 'group:admins', 'edit_all')]

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


# Pattern for matching string without special characters
# TODO: Put in utilities if there are more stuff
def has_special(string):
    import re
    return re.search(r"[^A-Za-z0-9_]+", string)


# TODO: BETTER SOLUTION
def groupfinder(userid, request):
    context = get_connection(request).root()['app_root']
    if userid in context['users']:
        return context['groups'][userid]


# Check if the user is logged in and allow access to admin
def user_access(login_required=True):
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            context, request = args
            logged_in = authenticated_userid(request)

            if login_required:
                # If the owner (or admin) isn't logged in: access denied
                if logged_in != context.username and not has_permission(
                                            'edit_all', context, request):
                    raise HTTPForbidden()
            return f(*args, user=logged_in)
        return wrapped_f
    return wrap


#Protect sessions from Cross-site request forgery attacks
@subscriber(NewRequest)
def csrf_validation(event):
    if event.request.method == "POST":
        token = event.request.POST.get("_csrf")
        if token is None or token != event.request.session.get_csrf_token():
            raise HTTPForbidden("CSRF token is missing or invalid")
