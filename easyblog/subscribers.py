from pyramid.renderers import get_renderer
from pyramid.interfaces import IBeforeRender
from pyramid.events import subscriber

@subscriber(IBeforeRender)
def add_base_template(event):
    base = get_renderer('templates/base.pt').implementation()
    news_widget = get_renderer('templates/news_widget.pt').implementation()
    event.update({'base': base, 'news_widget': news_widget})


