from zope.interface import Interface

class IComment(Interface):
    """ Marker interface. Enable comments. """

class IContainer(Interface):
    """ Mark the object as container.  """

class ISite(Interface):
    """ Marker interface. All the site objects must implement
    this interaface."""
