from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.renderers import get_renderer
from pyramid.url import resource_url
from pyramid.security import authenticated_userid
from pyramid.security import remember, forget
from easyblog.config import members_group
from easyblog.schemas import SignUpSchema, LoginSchema
from easyblog.schemas import UserEditSchema, BlogCreateSchema
from easyblog.schemas import BlogAddPostSchema, BaseSchema
from easyblog.schemas import UsersEditSchema
from easyblog.security import group_name
from easyblog.models import Main, User, Blog, Page, Blogs, Users
from easyblog.security import groupfinder
from easyblog.utilities import get_tool
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

# Handle news
def news():
    return u'news'

# Frontpage
@view_config(context=Main, renderer='templates/index.pt')
def view_main(request):
    logged_in = authenticated_userid(request)
    return {
        'layout': site_layout(),
        'project': 'easyblog',
        'logged_in': logged_in,
        'news': news()
    }


@view_config(context=Main, renderer='templates/signup.pt', name='signup')
def view_signup(context, request):
    """ Register view for new users that aren't signed up yet """
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
        context['groups'].add(username, u'u:%s' % username)

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

@view_config(context=Main, renderer='templates/login.pt', name='login')
@view_config(context='pyramid.exceptions.Forbidden',
             renderer='templates/login.pt')
def view_login(context, request):
    """ Login view """

    logged_in = authenticated_userid(request)
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

    if logged_in:
        message = msg['logged_in_as'] + logged_in + "."
    if context == HTTPForbidden:
        message += msg['content_forbidden']
    return {
        'message': message,
        'layout': site_layout(),
        'url': request.application_url + '/login',
        'came_from': came_from,
        'username': username,
        'password': password,
        'logged_in': logged_in,
        'form': FormRenderer(form)
    }


# Logout current user
@view_config(context=Main, renderer='templates/logout.pt', name='logout')
def view_logout(context, request):
    headers = forget(request)
    return HTTPFound(location=resource_url(request.context, request),
                    headers=headers)


# Page of the user. Some information about the user is rendered here.
@view_config(context=User, renderer='easyblog:templates/user_view.pt')
def view_user(context, request):
    logged_in = authenticated_userid(request)
    return {
        'layout': site_layout(),
        'project': 'easyblog',
        'username': context.username,
        'logged_in': logged_in,
    }


@view_config(name='edit', context=User, renderer='templates/user_edit.pt',
    permission='edit_user')
def view_user_edit(context, request):
    """ View for editing a single user """

    logged_in = authenticated_userid(request)
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
        'logged_in': logged_in,
        'form': FormRenderer(form),
        'email': context.email
    }

# TODO: Remove
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
def view_blog(context, request):
    logged_in = authenticated_userid(request)

    return {
        'logged_in': logged_in,
        'layout': site_layout(),
        'blogname': context.name,
        'posts': context
    }

@view_config(context=Blogs,
             renderer='templates/blogs_view.pt')
def view_blogs(context, request):
    """ View for all the blogs """

    logged_in = authenticated_userid(request)
    return {
        'page': context,
        'logged_in': logged_in,
        'layout': site_layout(),
        'context_url': resource_url(context, request),
        'resource_url': resource_url
    }


@view_config(context=Blogs, renderer='templates/blog_create.pt',
             permission='edit_all', name="create")
def view_blog_create(context, request):
    """ View for creating a single blog """
    logged_in = authenticated_userid(request)
    form = Form(request, schema=BlogCreateSchema, state=State(request=request))
    message = ''

    if form.validate():
        context.add(request.params['blogname'], logged_in)
        return HTTPFound(location=resource_url(context, request))

    return {
        'page': context,
        'logged_in': logged_in,
        'layout': site_layout(),
        'form': FormRenderer(form),
        'message': message
    }


@view_config(context=Blog, renderer='templates/blog_edit.pt',
             permission='edit_blog', name='edit')
def view_blog_edit(context, request):
    logged_in = authenticated_userid(request)
    message = "Edit %s" % context.name
    return {
        'page': context,
        'logged_in': logged_in,
        'layout': site_layout(),
        'blogname': context.name,
        'message': message
    }


@view_config(context=Blog, renderer='templates/blog_add_post.pt',
             permission='edit_blog', name='add_post')
def view_blog_add_post(context, request):
    logged_in = authenticated_userid(request)
    form = Form(request, schema=BlogAddPostSchema,
                state=State(request=request))
    message = "Edit %s" % context.name

    if form.validate():
        context.add(request.params['subject'], request.params['text'], logged_in)
        return HTTPFound(location=resource_url(context, request))

    return {
        'page': context,
        'logged_in': logged_in,
        'layout': site_layout(),
        'blogname': context.name,
        'message': message,
        'form': FormRenderer(form)
    }

@view_config(context=Blog, renderer='templates/blog_remove.pt',
             permission='edit_blog', name='remove')
def view_blog_remove(context, request):
    """ The Blog can be removed from this view """

    logged_in = authenticated_userid(request)
    form = Form(request, schema=BaseSchema,
                state=State(request=request))
    message = "Edit %s" % context.name

    if form.validate():
        return HTTPFound(location=resource_url(context.__parent__, request))

    return {
        'page': context,
        'logged_in': logged_in,
        'layout': site_layout(),
        'blogname': context.name,
        'message': message,
        'form': FormRenderer(form)
    }

@view_config(context=Users, renderer='templates/users_edit.pt',
             permission='edit_all', name='edit')
def view_users_edit(context, request):
    """ View for editing users. Includes permission handling. """

    logged_in = authenticated_userid(request)
    form = Form(request, schema=UsersEditSchema,
                state=State(request=request))

    message = "No search results"
    search_results = []
    if form.validate():
        search = request.params['search']

        # Loop through all the users and create dict of groups
        for user in context:
            if search in context[user].username:
                search_results.append(context[user])

        if request.params['submit'] == 'Save':
            # Filter checkbox-parameters from request
            cbs = [p for p in request.params.keys()
                        if u'checkbox' in p]

            # new policy for groups
            updated = {}

            # check all the checkbox-parameters and
            # parse them
            for cb in cbs:
                username = cb.split(':')[1]
                try:
                    updated[username]
                except KeyError:
                    updated[username] = []
                updated[username] += [request.params[cb]]

            groups_tool = get_tool('groups', request)
            groups_tool.add_policy(updated)

    # function for checking the group of the user
    def has_group(group, user, request):
        return group_name[group] in groupfinder(user.username, request)

    if search_results:
        message = "%d results found" % len(search_results)

    return {
        'page': context,
        'logged_in': logged_in,
        'layout': site_layout(),
        'form': FormRenderer(form),
        'search_results': search_results,
        'message': message,
        'group_name': group_name,
        'has_group': has_group
    }
