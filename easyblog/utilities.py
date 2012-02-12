def has_special(string):
    import re
    return re.search(r"[^A-Za-z0-9_]+", string)

# Returns content-objects from the database
# Use this whenever you must get a specific object from ZODB
# instead of travelling with __parent__ attributes
def get_resource(resource, request):
    root = request.root
    options = {
        'groups': root['groups'],
        'users': root['users'],
        'news': root['news']
    }
    return options[resource]

def get_param(request, name, _return=u''):
    value = _return
    try:
        value = request.params[name]
    except KeyError:
        pass
    return value

def shorten_text(text, word_count):
    # is there way to substring at a specific character?
    _list = text.split(" ")
    return " ".join(_list[0:word_count])


