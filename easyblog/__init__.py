from pyramid_zodbconn import get_connection
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from easyblog.models import appmaker
from easyblog.security import groupfinder

def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())

def main(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    authn_policy = AuthTktAuthenticationPolicy(secret='sosecret',
                                               callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(root_factory=root_factory, settings=settings,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    config.scan()
    return config.make_wsgi_app()
