from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.view import view_config
from pyramid.renderers import get_renderer
from pyramid.url import resource_url
from pyramid.security import authenticated_userid, remember, forget, has_permission

from easyblog.models import Main, User
from easyblog.config import members_group


# Define main layout for page
def site_layout():
    renderer = get_renderer("templates/main_layout.pt")
    layout = renderer.implementation().macros['layout']
    return layout

# Frontpage
@view_config(name='index', renderer='templates/index.pt')
def main_view(request):
    return {
        'layout': site_layout(),
        'project':'easyblog'
    }

@view_config(context=Main, renderer='templates/signup.pt', name='signup')
def signup(context, request):
    message = u''
    username = u''
    password = u''
    if 'form.submitted' in request.params:
        username = request.params['username']
        password = request.params['password']
        context['users'].add(username, password)
        context['groups'].add(username, members_group)
        message = 'Successfully added user: ' + username

    return {
        'message':message,
        'layout': site_layout(),
        'url': request.application_url + '/signup',
        'username': username,
        'password': password,
    }


@view_config(context=Main, renderer='templates/login.pt', name='login')
def login(context, request):
    username_url = resource_url(request.context, request, 'username')
    referrer = request.url
    if referrer == username_url:
        referrer = '/' # never use the username form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    username = ''
    password = ''
    if 'form.submitted' in request.params:
        username = request.params['username']
        password = request.params['password']
        try:
            if context['users'][username].validate_password(password):
                headers = remember(request, username)
                return HTTPFound(location = came_from,
                                 headers = headers)
        except KeyError:
            pass
        message = 'Failed username'

    return {
        'message': message,
        'layout': site_layout(),
        'url': request.application_url + '/login',
        'came_from': came_from,
        'username': username,
        'password': password,
    }

@view_config(context=Main, renderer='templates/logout.pt', name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = resource_url(request.context, request),
                    headers=headers)

@view_config(context=User, renderer='easyblog:templates/user_view.pt')
def user_view(context, request):
    username = context.username
    print authenticated_userid(request)
    return {
        'layout': site_layout(),
        'project':'easyblog',
        'username': username,
    }

@view_config(name='edit', context=User, renderer='templates/user_edit.pt',
    permission='edit')
def user_edit(context, request):
    username = context.username
    logged_in = authenticated_userid(request)

    # Allow access only for the user of the page
    if logged_in != username and not has_permission('edit_all', context,request):
        return HTTPForbidden()
    return {
        'layout': site_layout(),
        'project':'easyblog',
        'username': username,
    }

@view_config(context='.models.Page',
             renderer='templates/page.pt', permission='edit')
def view_page(context, request):
    wiki = context.__parent__

    logged_in = authenticated_userid(request)

    return dict(page = context, logged_in = logged_in, layout = site_layout())


