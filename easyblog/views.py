from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.renderers import get_renderer
from pyramid.url import resource_url
from pyramid.security import authenticated_userid
from pyramid.security import remember, forget
from easyblog.schemas import SignUpSchema, LoginSchema
from easyblog.schemas import UserEditSchema, BlogCreateSchema
from easyblog.schemas import BlogAddPostSchema
from easyblog.models import Main, User, Blog, Page, Blogs
from easyblog.config import members_group
from easyblog.security import user_access
from pyramid_simpleform.renderers import FormRenderer
from pyramid_simpleform import Form, State
from pyramid.httpexceptions import HTTPForbidden

# Messages
from easyblog.config import msg


# Define main layout for page
def site_layout():
    renderer = get_renderer("templates/main_layout.pt")
    layout = renderer.implementation().macros['layout']
    return layout


# Frontpage
@view_config(context=Main, renderer='templates/index.pt')
def view_main(request):
    logged_in = authenticated_userid(request)
    return {
        'layout': site_layout(),
        'project': 'easyblog',
        'logged_in': logged_in
    }


# Register form for new users that aren't signed up yet
@view_config(context=Main, renderer='templates/signup.pt', name='signup')
def view_signup(context, request):
    logged_in = authenticated_userid(request)
    message = u''
    username = u''
    password = u''

    # Create form by using schemas with validations
    form = Form(request, schema=SignUpSchema, state=State(request=request))

    # form.validate() doesn't work with tests that use url-parameters
    if form.validate():
        username = request.params['username']
        password = request.params['password']
        email = request.params['email']
        context['users'].add(username, password, email)
        context['groups'].add(username, members_group)
        message = msg['succeed_add_user'] + username

    return {
        'message': message,
        'layout': site_layout(),
        'url': request.application_url + '/signup',
        'username': username,
        'logged_in': logged_in,
        'password': password,
        'form': FormRenderer(form)
    }
    return None


# Handle's user login
@view_config(context=Main, renderer='templates/login.pt', name='login')
@view_config(context='pyramid.exceptions.Forbidden',
             renderer='templates/login.pt')
@user_access(login_required=False)
def view_login(context, request, user):
    login_url = resource_url(request.context, request, 'login')
    referrer = request.url
    if referrer == login_url:
        # never use the login form itself as came_from
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    message = ''
    username = ''
    password = ''

    # Create form by using schemas with validations
    form = Form(request, schema=LoginSchema, state=State(request=request))

    if form.validate():
        username = request.params['username']
        password = request.params['password']
        try:
            if context['users'][username].validate_password(password):
                headers = remember(request, username)
                return HTTPFound(location=came_from,
                                 headers=headers)
        except KeyError:
            pass
        message = 'Failed username'

    if user:
        message = msg['logged_in_as'] + user + "."
    if context == HTTPForbidden:
        message += msg['content_forbidden']
    return {
        'message': message,
        'layout': site_layout(),
        'url': request.application_url + '/login',
        'came_from': came_from,
        'username': username,
        'password': password,
        'logged_in': user,
        'form': FormRenderer(form)
    }


# Logout current user
@view_config(context=Main, renderer='templates/logout.pt', name='logout')
@user_access(login_required=False)
def view_logout(context, request, user):
    headers = forget(request)
    return HTTPFound(location=resource_url(request.context, request),
                    headers=headers)


# Page of the user. Some information about the user is rendered here.
@view_config(context=User, renderer='easyblog:templates/user_view.pt')
@user_access(login_required=False)
def view_user(context, request, user):
    return {
        'layout': site_layout(),
        'project': 'easyblog',
        'username': context.username,
        'logged_in': user,
    }


# View for editing single user
@view_config(name='edit', context=User, renderer='templates/user_edit.pt',
    permission='edit')
@user_access(login_required=True)
def view_user_edit(context, request, user):
    message = ''
    form = Form(request, schema=UserEditSchema, state=State(request=request))

    if form.validate():
        password = request.params['password']
        if context.validate_password(password):
            if request.params['new_password']:
                password = request.params['new_password']
            message = 'Successfully saved'
            email = request.params['email']
            context.edit(password, email)
        else:
            message = msg['password_invalid']
    return {
        'message': message,
        'layout': site_layout(),
        'project': 'easyblog',
        'username': context.username,
        'logged_in': user,
        'form': FormRenderer(form),
        'email': context.email
    }


@view_config(context=Page,
             renderer='templates/page.pt', permission='edit')
def view_page(context, request):
    logged_in = authenticated_userid(request)

    return {
        'page': context,
        'logged_in': logged_in,
        'layout': site_layout(),
    }


@view_config(context=Blog,
             renderer='templates/blog_view.pt')
@user_access(login_required=False)
def view_blog(context, request, user):
    return {
        'logged_in': user,
        'layout': site_layout(),
        'blogname': context.name,
        'posts': context.blogposts
    }


@view_config(context=Blogs,
             renderer='templates/blogs_view.pt')
@user_access(login_required=False)
def view_blogs(context, request, user):
    return {
        'page': context,
        'logged_in': user,
        'layout': site_layout(),
        'blogs': context
    }


@view_config(context=Blogs, renderer='templates/blog_create.pt',
             permission='edit', name="create")
@user_access(login_required=False)
def view_blog_create(context, request, user):
    form = Form(request, schema=BlogCreateSchema, state=State(request=request))
    message = ''

    if form.validate():
        context.add(request.params['blogname'], user)

    return {
        'page': context,
        'logged_in': user,
        'layout': site_layout(),
        'form': FormRenderer(form),
        'message': message
    }


@view_config(context=Blog, renderer='templates/blog_edit.pt',
             permission='edit', name='edit')
@user_access(login_required=True)
def view_blog_edit(context, request, user):
    message = "Edit %s" % context.name
    return {
        'page': context,
        'logged_in': user,
        'layout': site_layout(),
        'blogname': context.name,
        'message': message
    }


@view_config(context=Blog, renderer='templates/blog_add_post.pt',
             permission='edit', name='add_post')
@user_access(login_required=True)
def view_blog_add_post(context, request, user):
    form = Form(request, schema=BlogAddPostSchema,
                state=State(request=request))
    message = "Edit %s" % context.name

    if form.validate():
        context.add(request.params['subject'], request.params['text'], user)
        return HTTPFound(location=resource_url(context, request))

    return {
        'page': context,
        'logged_in': user,
        'layout': site_layout(),
        'blogname': context.name,
        'message': message,
        'form': FormRenderer(form)
    }
