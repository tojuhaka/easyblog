from zope.interface import Interface

class IComment(Interface):
    """ Marker interface. Enable comments. """

class ISite(Interface):
    """ Marker interface. All the site objects must implement
    this interaface."""
