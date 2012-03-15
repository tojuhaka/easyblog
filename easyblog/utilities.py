# -*- coding: utf-8 -*-
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
        'news': root['news'],
        'root': root
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

def provides(context, interface):
    """ The main point of this function is to avoid returning interfaces
    to the template. Instead we return one function which can be used
    to check if context provides an interface. The interface is given
    as string """

    from easyblog.interfaces import IAbout, IContact, IBlogs, INews, ISiteRoot
    _dict = {
        'IBlogs': IBlogs.providedBy(context),
        'INews': INews.providedBy(context),
        'IAbout': IAbout.providedBy(context),
        'IContact': IContact.providedBy(context),
        'ISiteRoot': ISiteRoot.providedBy(context),
    }
    return _dict[interface]


# There are some cases where we can't translate properly.
# For example 'blogs' and 'news' in breadcrumbs cannot be
# translated
def translate(s, lang):
    _dict = {
        'blogs': {'fi': u'Blogit'},
        'news': {'fi': u'Uutiset'},
        'about': {'fi': u'Meistä'},
        'contact': {'fi': u'Yhteystiedot'},
    }
    try: 
        translated = _dict[s][lang]
    except KeyError:
        translated = s
    return translated


