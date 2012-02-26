from zope.interface import Interface

class IComment(Interface):
    """ Marker interface. Enable comments. """

class IContainer(Interface):
    """ Mark the object as container.  """

class IContent(Interface):
    """ Mark the object as container.  """

class IPage(Interface):
    """ Mark the object as page """

class ISiteRoot(Interface):
    """ Marker interface. All the site objects must implement
    this interaface."""
