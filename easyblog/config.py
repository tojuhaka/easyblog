from pyramid_zodbconn import get_connection

members_group = ['group:members']
admins_group = ['group:admins']
editors_group = ['group:editors']

# TODO: move to utilities
def get_tool(tool, request):
    root = get_connection(request).root()['app_root']
    options = {
        'groups': root['groups']
    }
    return options[tool]

msg = {
    'content_forbidden':  u"You have no permission to review this content",
    'password_invalid':  u"Password is invalid.",
    'logged_in_as': u"You are logged in as",
    'succeed_add_user': u"Successfully added user",
    'saved': u"Successfully saved",
    }

