from pyramid_zodbconn import get_connection

# Pattern for matching string without special characters
def has_special(string):
    import re
    return re.search(r"[^A-Za-z0-9_]+", string)

# Returns content-objects from the database
# Use this whenever you must get a specific object from ZODB
# instead of travelling with __parent__ attributes
def get_tool(tool, request):
    root = get_connection(request).root()['app_root']
    options = {
        'groups': root['groups'],
        'users': root['users']
    }
    return options[tool]

