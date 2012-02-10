from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.security import authenticated_userid
from pyramid.security import remember, forget
from .schemas import SignUpSchema, LoginSchema
from .schemas import UserEditSchema, BlogCreateSchema
from .schemas import BlogPostSchema, BaseSchema
from .schemas import UsersEditSchema, NewsCreateSchema
from .security import group_names
from .models import Main, User, Blog, Blogs
from .models import Users, News, BlogPost, NewsItem
from .security import groupfinder
from .utilities import get_resource, get_param
from pyramid_simpleform.renderers import FormRenderer
from pyramid_simpleform import Form, State
from pyramid.httpexceptions import HTTPForbidden

# Messages
from .config import msg
from .interfaces import ISiteRoot, IComment, IContainer, IContent

from pyramid.security import has_permission


class MainView(object):
    """ View for managing Main-object (root, frontpage) """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=Main, renderer='templates/index.pt')
    def view_frontpage(self):
        #TODO: make content type for frontpage
        """ FrontPage """
        logged_in = authenticated_userid(self.request)
        return {
            'project': '',
            'logged_in': logged_in,

        }

    @view_config(context=Main, renderer='templates/signup.pt', name='signup')
    def view_signup(self):
        """ Register view for new users that aren't signed up yet """
        logged_in = authenticated_userid(self.request)
        message = u''
        username = get_param(self.request, 'username')
        email = get_param(self.request, 'email')
        password = u''

        # if logged in don't show the signup form
        if logged_in:
            message = msg['logged_in_as'] + " " + logged_in

        # Create form by using schemas with validations
        form = Form(self.request, schema=SignUpSchema,
                state=State(request=self.request))

        if form.validate():
            username = self.request.params['username']
            password = self.request.params['password']
            email = self.request.params['email']
            self.context['users'].add(username, password, email)
            self.context['groups'].add(username, group_names['member'])
            self.context['groups'].add(username, u'u:%s' % username)

            message = msg['succeed_add_user'] + " " + username

        return {
            'message': message,
            'url': self.request.application_url + '/signup',
            'username': username,
            'email': email,
            'logged_in': logged_in,
            'password': password,
            'form': FormRenderer(form),
            'params': self.request.params
        }

    @view_config(context=Main, renderer='templates/login.pt', name='login')
    @view_config(context='pyramid.exceptions.Forbidden',
                 renderer='templates/login.pt')
    def view_login(self):
        """ Login view """

        logged_in = authenticated_userid(self.request)
        login_url = resource_url(self.request.context, self.request, 'login')
        referrer = self.request.url
        if referrer == login_url:
            # never use the login form itself as came_from
            referrer = '/'
        came_from = self.request.params.get('came_from', referrer)
        message = ''
        username = ''
        password = ''

        # Create form by using schemas with validations
        form = Form(self.request, schema=LoginSchema,
                state=State(request=self.request),
                defaults={'klass': 'class'})

        if form.validate():
            username = self.request.params['username']
            password = self.request.params['password']
            try:
                if self.context['users'][username].validate_password(password):
                    headers = remember(self.request, username)
                    return HTTPFound(location=came_from,
                                     headers=headers)
            except KeyError:
                pass
            message = 'Failed username'

        if logged_in:
            message = msg['logged_in_as'] + logged_in + ". "

        if  type(self.context) == HTTPForbidden:
            message += msg['content_forbidden']

        return {
            'message': message,
            'url': self.request.application_url + '/login',
            'came_from': came_from,
            'username': username,
            'password': password,
            'logged_in': logged_in,
            'form': FormRenderer(form)
        }

    @view_config(context=Main, renderer='templates/logout.pt', name='logout')
    def view_logout(self):
        """ Logout current user """
        headers = forget(self.request)
        return HTTPFound(location=resource_url(self.request.context,
                        self.request), headers=headers)


class UserView(object):
    """ View for single user """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=User, renderer='templates/user_view.pt')
    def view_user(self):
        """ Main view for user """

        logged_in = authenticated_userid(self.request)
        return {
            'project': '',
            'username': self.context.username,
            'logged_in': logged_in,
        }

    @view_config(name='edit', context=User, renderer='templates/user_edit.pt',
        permission='edit_content')
    def view_user_edit(self):
        """ View for editing a single user """

        logged_in = authenticated_userid(self.request)
        message = ''
        form = Form(self.request, schema=UserEditSchema,
                state=State(request=self.request))

        if form.validate():
            password = self.request.params['password']
            if self.context.validate_password(password):
                if self.request.params['new_password']:
                    password = self.request.params['new_password']
                message = 'Successfully saved'
                email = self.request.params['email']
                self.context.edit(password, email)
            else:
                message = msg['password_invalid']
        return {
            'message': message,
            'project': '',
            'username': self.context.username,
            'logged_in': logged_in,
            'form': FormRenderer(form),
            'email': self.context.email
        }


class BlogPost(object):
    """ View for single blogpost """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=BlogPost,
                 renderer='templates/blogpost.pt')
    def __call__(self):
        logged_in = authenticated_userid(self.request)
        return {
            'logged_in': logged_in,
            'title': self.context.title,
            'text': self.context.text,
        }

    @view_config(context=BlogPost,
                 renderer='templates/blogpost_edit.pt', name="edit",
                 permission='edit_content')
    def view_blogpost_edit(self):
        logged_in = authenticated_userid(self.request)
        form = Form(self.request, schema=BlogPostSchema,
                    state=State(request=self.request))
        message = ""
        if form.validate():
            message = msg['saved']
            title = self.request.params[u'title']
            text = self.request.params[u'text']
            self.context.title = title
            self.context.text = text

        return {
            'message': message,
            'project': '',
            'title': self.context.title,
            'text': self.context.text,
            'logged_in': logged_in,
            'form': FormRenderer(form),
        }


class BlogView(object):
    """ View for single blog """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=Blog,
                 renderer='templates/blog_view.pt')
    def view_blog(self):
        logged_in = authenticated_userid(self.request)
        from pyramid_viewgroup import Provider
        return {
            'logged_in': logged_in,
            'blogname': self.context.name,
            'posts': self.context,
            'provider': Provider(self.context, self.request)
        }

    @view_config(context=Blog, renderer='templates/blog_edit.pt',
                 permission='edit_content', name='edit')
    def view_blog_edit(self):
        logged_in = authenticated_userid(self.request)
        message = "Edit %s" % self.context.name
        return {
            'page': self.context,
            'logged_in': logged_in,
            'blogname': self.context.name,
            'message': message
        }

    @view_config(context=Blog, renderer='templates/blog_create_post.pt',
                 permission='edit_content', name='create')
    #TODO: rename add_post to create
    def view_blog_add_post(self):
        logged_in = authenticated_userid(self.request)
        form = Form(self.request, schema=BlogPostSchema,
                    state=State(request=self.request))
        message = ""

        if form.validate():
            post_context = self.context.add(self.request.params['title'],
                        self.request.params['text'], logged_in)

            return HTTPFound(location=resource_url(post_context, self.request))

        return {
            'page': self.context,
            'logged_in': logged_in,
            'blogname': self.context.name,
            'message': message,
            'form': FormRenderer(form),
            'resource_url': resource_url
        }

    @view_config(context=Blog, renderer='templates/blog_remove.pt',
                 permission='edit_content', name='remove')
    def view_blog_remove(self):
        """ The Blog can be removed from this view """

        logged_in = authenticated_userid(self.request)
        form = Form(self.request, schema=BaseSchema,
                    state=State(request=self.request))
        message = "Edit %s" % self.context.name

        if form.validate():
            return HTTPFound(location=resource_url(self.context.__parent__,
                        self.request))

        return {
            'page': self.context,
            'logged_in': logged_in,
            'blogname': self.context.name,
            'message': message,
            'form': FormRenderer(form)
        }


class BlogsView(object):
    """ View for all the blogs """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=Blogs,
                 renderer='templates/blogs_view.pt')
    def __call__(self):
        """ View for all the blogs """

        logged_in = authenticated_userid(self.request)
        return {
            'page': self.context,
            'logged_in': logged_in,
            'context_url': resource_url(self.context, self.request),
            'resource_url': resource_url,
            'has_permission': has_permission('edit_container',
                            self.context, self.request)
        }

    @view_config(context=Blogs, renderer='templates/blog_create.pt',
                 permission='edit_container', name="create")
    def view_blog_create(self):
        """ View for creating a single blog """
        logged_in = authenticated_userid(self.request)
        form = Form(self.request, schema=BlogCreateSchema,
                    state=State(request=self.request))
        message = ''

        if form.validate():
            blog_context = self.context.add(self.request.params['blogname'],
                            logged_in)
            return HTTPFound(location=resource_url(blog_context, self.request))

        return {
            'page': self.context,
            'logged_in': logged_in,
            'form': FormRenderer(form),
            'message': message
        }


class UsersView(object):
    """ View for all the users """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=Users, renderer='templates/users_edit.pt',
                 permission='edit_all', name='edit')
    def view_users_edit(self):
        """ View for editing users. Includes permission handling. """

        logged_in = authenticated_userid(self.request)
        form = Form(self.request, schema=UsersEditSchema,
                    state=State(request=self.request))

        search_results = []
        message = u""
        search = u""

        if form.validate():
            search = self.request.params['search']

            # Loop through all the users and create dict of groups
            for user in self.context:
                if search.lower() in self.context[user].username.lower():
                    search_results.append(self.context[user])

            if 'save' in self.request.params.keys() and \
                    self.request.params['save'] == 'Save':
                message = msg['saved']
                # Filter checkbox-parameters from request
                cbs = [p for p in self.request.params.keys()
                            if u'checkbox' in p]
                users = [self.request.params[p] for p in
                        self.request.params.keys()
                            if u'user' == p]

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
                    updated[username] += [self.request.params[cb]]

                groups_tool = get_resource('groups', self.request)

                # Init users as empty first, then update with checkbox-data
                # TODO: add 'u:user' group?
                for user in users:
                    groups_tool.flush(user)
                groups_tool.add_policy(updated)

        def has_group(group, user, request):
            """ Check if the user belongs to the group """
            return group_names[group] in groupfinder(user.username, request)

        def sorted_gnames():
            """ Sort list of keys to make sure they are in right order """
            return sorted(group_names.keys())

        return {
            'page': self.context,
            'logged_in': logged_in,
            'form': FormRenderer(form),
            'search_results': search_results,
            'message': message,
            'group_names': group_names,
            'has_group': has_group,
            'sorted_gnames': sorted_gnames(),
            'result_count': len(search_results),
            'search_term': search
        }


class NewsWidget(object):
    """ Widget for news. It's shown in every page inside
    base template"""
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=ISiteRoot, name="news_widget",
            renderer='templates/news_widget.pt')
    def __call__(self):
        news = self.context['news'].order_by_time()
        news_number = 3
        
        from .utilities import shorten_text
        return {
            'news': news[0:news_number],
            'resource_url': resource_url,
            'shorten': shorten_text
        }


class NewsItem(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=NewsItem, renderer='templates/news_item.pt')
    def __call__(self):
        logged_in = authenticated_userid(self.request)
        return {
            'title': self.context.title,
            'text': self.context.text,
            'logged_in': logged_in,
            'resource_url': resource_url,
        }


class NewsView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=News, renderer='templates/news.pt')
    def __call__(self):
        logged_in = authenticated_userid(self.request)
        return {
            'news': self.context,
            'logged_in': logged_in,
            'resource_url': resource_url,
        }

    @view_config(context=News, name="create",
                renderer='templates/news_create.pt',
                permission="edit_container")
    def view_news_create(self):
        logged_in = authenticated_userid(self.request)
        form = Form(self.request, schema=NewsCreateSchema,
                    state=State(request=self.request))
        title = get_param(self.request, 'title')
        text = get_param(self.request, 'text')
        image_url = get_param(self.request, 'image_url')

        if form.validate():
            item_context = self.context.add(title, text, image_url, logged_in)
            return HTTPFound(location=resource_url(item_context, self.request))

        return {
            'page': self.context,
            'logged_in': logged_in,
            'context_url': resource_url(self.context, self.request),
            'resource_url': resource_url,
            'form': FormRenderer(form),
            'title': title,
            'content': text,
            'image_url': image_url,
        }

    @view_config(context=News, name="edit",
                renderer='templates/news_edit.pt', permission="edit_container")
    def view_news_edit(self):
        logged_in = authenticated_userid(self.request)
        form = Form(self.request, schema=BaseSchema,
                    state=State(request=self.request))
        message = ""
        if form.validate():
            # Filter checkbox-parameters from request
            cbs = [p for p in self.request.params.keys()
                            if u'checkbox' in p]

            # check all the checkbox-parameters and
            # parse them
            for cb in cbs:
                item = self.request.params[cb]
                self.context.remove(item)
                message = msg['items_removed']

        return {
            'page': self.context,
            'logged_in': logged_in,
            'context_url': resource_url(self.context, self.request),
            'resource_url': resource_url,
            'form': FormRenderer(form),
            'message': message,
        }


class EditBarView(object):
    """ View for editbars in container and
    content objects """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=IContainer, name="editbar",
            renderer='templates/container_editbar.pt')
    def view_container_bar(self):
        """ Bar for container """
        return {
            'edit_url': resource_url(self.context, self.request) + 'edit',
            'create_url': resource_url(self.context, self.request) + 'create',
            'has_permission': has_permission('edit_container',
                            self.context, self.request)
        }

    @view_config(context=IContent, name="editbar",
            renderer='templates/content_editbar.pt')
    def view_content_bar(self):
        """ Bar for single content """
        return {
            'edit_url': resource_url(self.context, self.request) + 'edit',
            'has_permission': has_permission('edit_content',
                            self.context, self.request)
        }


class CommentView(object):
    """ View for comments """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=IComment, name="comments",
            renderer='templates/comments.pt')
    def __call__(self):
        return {
            'comments': self.context.comments
        }

    @view_config(context=IComment, name="add_comment")
    def add_comment(self):
        return {
            'asdf': 'asdf'
        }
