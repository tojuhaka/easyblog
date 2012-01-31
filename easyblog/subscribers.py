from pyramid.renderers import get_renderer
from pyramid.interfaces import IBeforeRender
from pyramid.events import subscriber
from pyramid_viewgroup import Provider

@subscriber(IBeforeRender)
def add_base_template(event):
    base = get_renderer('templates/base.pt').implementation()
    event.update({
        'base': base,
        'provider': Provider(event['context'], event['request'])
    })


