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


def order(context, ordered_keys):
    ordered = []
    for key in ordered_keys:
        news_item = context[key]
        ordered.append(news_item)
    return ordered

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]


class Provider(object):
    """ Provides rendered pages inside other templates """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, name='', secure=True):
        from pyramid.view import render_view
        # Decode to utf8, else it's gonna throw UnicodeDecodeError
        try:
            return render_view(self.context, self.request,
                    name, secure).decode("utf8")
        except AttributeError:
            pass
        return None


