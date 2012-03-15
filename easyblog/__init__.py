from pyramid.config import Configurator
from pyramid_zodbconn import get_connection

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import appmaker
from .security import groupfinder
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('easyblog')


def my_locale_negotiator(request):
    # TODO: make translation links to site
    locale_name = 'en'
    return locale_name

def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """

    # TODO: make it safer. Remember it's unencrypted.
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseecreet')
    authn_policy = AuthTktAuthenticationPolicy(secret='sosecret',
                                               callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(session_factory=my_session_factory,
                          root_factory=root_factory, settings=settings,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    config.add_translation_dirs('easyblog:locale/')
    config.set_locale_negotiator(my_locale_negotiator)
    config.add_settings(encoding="UTF-8")
    # config.add_settings(languages=['fi', 'en'])
    # config.add_settings({'default_locale_name': 'fi'})
    config.add_settings(default_encoding="UTF-8")
    config.hook_zca()

    config.include('pyramid_viewgroup')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()
    return config.make_wsgi_app()
