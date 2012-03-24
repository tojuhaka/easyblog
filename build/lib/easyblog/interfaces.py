from zope.interface import Interface
# We should have used more ZCA in this application. 
# Atleast there are some interfaces. 

class IComment(Interface):
    """ Marker interface. Enable comments. """

class IContainer(Interface):
    """ Mark the object as container.  """

class IContent(Interface):
    """ Mark the object as container.  """

class IPage(Interface):
    """ Mark the object as page """

class INavPage(Interface):
    """ Mark the object as navigation object. It's shown
    in nav bar """

class ISiteRoot(Interface):
    """ Marker interface. All the site objects must implement
    this interaface."""

class IAbout(Interface):
    """ About is a single page which has some information
    about the client """

class IContact(Interface):
    """ About is a single page which has some information
    about the client """

class IAbout(Interface):
    """ About is a single page which has some information
    about the client """

class IBlogs(Interface):
    """ Blogs is a container for multiple blogs """

class INews(Interface):
    """ News is a container for multiple news item """

