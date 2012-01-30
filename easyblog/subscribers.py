from pyramid.renderers import get_renderer
from pyramid.interfaces import IBeforeRender
from pyramid.events import subscriber
from easyblog.interfaces import IComment
from zope.interface.verify import verifyObject
from zope.interface.exceptions import DoesNotImplement

@subscriber(IBeforeRender)
def add_base_template(event):
    base = get_renderer('templates/base.pt').implementation()
    comments = get_renderer('templates/comments.pt').implementation()
    event.update({'base': base, 'comments_template': comments})

@subscriber(IBeforeRender)
def add_comments(event):
    """ Check if the context implements IComment and
    add comments to it """
    try:
        verifyObject(IComment, event['context'])
        event.update({'comments': event['context'].comments})
    except DoesNotImplement:
        event.update({'comments': None})
        """ Ignore """
    except AttributeError:
        event.update({'comments': None})
        

