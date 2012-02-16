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
from .utilities import shorten_text
from pyramid_simpleform.renderers import FormRenderer
from pyramid_simpleform import Form, State
from pyramid.httpexceptions import HTTPForbidden

# Messages
from .config import msg
from .interfaces import ISiteRoot, IComment, IContainer, IContent

from pyramid.security import has_permission


class BaseView(object):
    """ Base view for everything. Defines some
    basic attributes and functions that are used
    in every view """
    def __init__(self, context, request):
        self.context = context
        self.request = request

        # Logged User
        self.logged_in = authenticated_userid(request)

        # Main message for pages if needed
        self.message = u''

        from pyramid.renderers import get_renderer
        from easyblog.utilities import Provider
        base = get_renderer('templates/base.pt').implementation()
        # This dict will be returned in every view
        self.base_dict = {
            'logged_in': self.logged_in,
            'message': self.message,
            'resource_url': resource_url,
            'base': base,
            'provider': Provider(self.context, self.request)
        }


class MainView(BaseView):
    """ View for managing Main-BaseView (root, frontpage) """

    @view_config(context=Main, renderer='templates/index.pt')
    def view_frontpage(self):
        #TODO: make content type for frontpage
        """ FrontPage """
        return self.base_dict

    @view_config(context=Main, renderer='templates/signup.pt', name='signup')
    def view_signup(self):
        """ Register view for new users that aren't signed up yet """
        username = get_param(self.request, 'username')
        email = get_param(self.request, 'email')
        password = u''

        # if logged in don't show the signup form
        if self.logged_in:
            self.message = msg['logged_in_as'] + " " + self.logged_in

        # Create form by using schemas with validations
        form = Form(self.request, schema=SignUpSchema,
                state=State(request=self.request))

        if form.validate():
            username = self.request.params['username']
            password = self.request.params['password']
            email = self.request.params['email']
            get_resource('users', self.request).add(username,
                    password, email)
            get_resource('groups', self.request).add(username,
                    group_names['member'])
            get_resource('groups', self.request).add(username,
                    u'u:%s' % username)
            self.message = msg['succeed_add_user'] + " " + username

        _dict = {
            'url': self.request.application_url + '/signup',
            'username': username,
            'email': email,
            'password': password,
            'form': FormRenderer(form),
            'params': self.request.params,
            'message': self.message
        }
        return dict(self.base_dict.items() + _dict.items())

    @view_config(context=Main, renderer='templates/login.pt', name='login')
    @view_config(context='pyramid.exceptions.Forbidden',
                 renderer='templates/login.pt')
    def view_login(self):
        """ Login view """
        login_url = resource_url(self.request.context, self.request, 'login')
        referrer = self.request.url
        if referrer == login_url:
            # never use the login form itself as came_from
            referrer = '/'
        came_from = self.request.params.get('came_from', referrer)
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
            self.message = 'Failed username'

        if self.logged_in:
            self.message = msg['logged_in_as'] + self.logged_in + ". "

        if  type(self.context) == HTTPForbidden:
            self.message += msg['content_forbidden']

        _dict = {
            'url': self.request.application_url + '/login',
            'came_from': came_from,
            'username': username,
            'password': password,
            'form': FormRenderer(form),
            'message': self.message
        }
        return dict(self.base_dict.items() + _dict.items())

    @view_config(context=Main, renderer='templates/logout.pt', name='logout')
    def view_logout(self):
        """ Logout current user """
        headers = forget(self.request)
        return HTTPFound(location=resource_url(self.request.context,
                        self.request), headers=headers)


class UserView(BaseView):
    """ View for single user """

    @view_config(context=User, renderer='templates/user_view.pt')
    def view_user(self):
        """ Main view for user """
        _dict = {
            'username': self.context.username,
        }
        return dict(self.base_dict.items() + _dict.items())

    @view_config(name='edit', context=User, renderer='templates/user_edit.pt',
        permission='edit_content')
    def view_user_edit(self):
        """ View for editing a single user """

        form = Form(self.request, schema=UserEditSchema,
                state=State(request=self.request))

        if form.validate():
            password = self.request.params['password']
            if self.context.validate_password(password):
                if self.request.params['new_password']:
                    password = self.request.params['new_password']
                self.message = 'Successfully saved'
                email = self.request.params['email']
                self.context.edit(password, email)
            else:
                self.message = msg['password_invalid']

        _dict = {
            'username': self.context.username,
            'form': FormRenderer(form),
            'email': self.context.email,
            'message': self.message
        }
        return dict(self.base_dict.items() + _dict.items())


class BlogPost(BaseView):
    """ View for single blogpost """

    @view_config(context=BlogPost,
                 renderer='templates/blogpost.pt')
    def __call__(self):
        return self.base_dict

    @view_config(context=BlogPost,
                 renderer='templates/blogpost_edit.pt', name="edit",
                 permission='edit_content')
    def view_blogpost_edit(self):
        form = Form(self.request, schema=BlogPostSchema,
                    state=State(request=self.request))
        if form.validate():
            self.message = msg['saved']
            title = self.request.params[u'title']
            text = self.request.params[u'text']
            self.context.title = title
            self.context.text = text

        _dict = {
            'project': '',
            'title': self.context.title,
            'text': self.context.text,
            'form': FormRenderer(form),
            'message': self.message
        }
        return dict(self.base_dict.items() + _dict.items())


class BlogView(BaseView):
    """ View for single blog """

    @view_config(context=Blog,
                 renderer='templates/blog_view.pt')
    def view_blog(self):
        from pyramid_viewgroup import Provider
        _dict = {
            'blogname': self.context.name,
            'provider': Provider(self.context, self.request),
            'container': self.context.description,
            'image_url': self.context.image_url,
        }
        return dict(self.base_dict.items() + _dict.items())

    @view_config(context=Blog, renderer='templates/blog_edit.pt',
                 permission='edit_content', name='edit')
    def view_blog_edit(self):
        self.message = "Edit %s" % self.context.name
        _dict = {
            'page': self.context,
            'blogname': self.context.name,
            'message': self.message
        }
        return dict(self.base_dict.items() + _dict.items())

    @view_config(context=Blog, renderer='templates/blog_create_post.pt',
                 permission='edit_content', name='create')
    #TODO: rename add_post to create
    def view_blog_add_post(self):
        form = Form(self.request, schema=BlogPostSchema,
                    state=State(request=self.request))
        message = msg['create_post']

        title = get_param(self.request, 'title')
        text = get_param(self.request, 'text')

        if form.validate():
            post_context = self.context.add(title,
                        text, self.logged_in)

            return HTTPFound(location=resource_url(post_context, self.request))

        _dict = {
            'page': self.context,
            'blogname': self.context.name,
            'text': text,
            'title': title,
            'message': message,
            'form': FormRenderer(form),
        }
        return dict(self.base_dict.items() + _dict.items())

    @view_config(context=Blog, renderer='templates/blog_remove.pt',
                 permission='edit_content', name='remove')
    def view_blog_remove(self):
        """ The Blog can be removed from this view """

        form = Form(self.request, schema=BaseSchema,
                    state=State(request=self.request))
        self.message = "Edit %s" % self.context.name

        if form.validate():
            return HTTPFound(location=resource_url(self.context.__parent__,
                        self.request))

        _dict = {
            'page': self.context,
            'blogname': self.context.name,
            'message': self.message,
            'form': FormRenderer(form)
        }
        return dict(self.base_dict.items() + _dict.items())


class BlogsView(BaseView):
    """ View for all the blogs """

    # blogs_view
    @view_config(context=Blogs,
                 renderer='templates/blogs_view_grid.pt')
    def __call__(self):
        """ View for all the blogs """

        # make list for image grid
        # in the grid there will be 3 items in a single row
        # we'll build a special list for this since it seems
        # quite hard trying to do it with chameleon
        from .utilities import chunks
        splitted_keys = chunks(self.context.keys(), 4)

        _dict = {
            'context_url': resource_url(self.context, self.request),
            'splitted_keys': splitted_keys,
            'shorten': shorten_text
        }
        return dict(self.base_dict.items() + _dict.items())

    @view_config(context=Blogs, renderer='templates/blog_create.pt',
                 permission='edit_container', name="create")
    def view_blog_create(self):
        """ View for creating a single blog """
        logged_in = authenticated_userid(self.request)
        form = Form(self.request, schema=BlogCreateSchema,
                    state=State(request=self.request))
        blogname = get_param(self.request, 'blogname')
        text = get_param(self.request, 'text')
        image_url = get_param(self.request, 'image_url')

        if form.validate():
            blog = self.context.add(blogname, text,
                    image_url, logged_in)
            return HTTPFound(location=resource_url(blog, self.request))

        _dict = {
            'form': FormRenderer(form),
            'message': self.message,
            'blogname': blogname,
            'text': text,
            'image_url': image_url
        }
        return dict(self.base_dict.items() + _dict.items())

    @view_config(context=News, name="edit",
                renderer='templates/blogs_edit.pt',
                permission="edit_container")
    def view_blogs_edit(self):
        form = Form(self.request, schema=BaseSchema,
                    state=State(request=self.request))
        if form.validate():
            # Filter checkbox-parameters from request
            cbs = [p for p in self.request.params.keys()
                            if u'checkbox' in p]

            # check all the checkbox-parameters and
            # parse them
            for cb in cbs:
                item = self.request.params[cb]
                self.context.remove(item)
                self.message = msg['items_removed']

        _dict = {
            'context_url': resource_url(self.context, self.request),
            'form': FormRenderer(form),
            'message': self.message,
        }
        return dict(self.base_dict.items() + _dict.items())


class UsersView(BaseView):
    """ View for all the users """

    @view_config(context=Users, renderer='templates/users_edit.pt',
                 permission='edit_all', name='edit')
    def view_users_edit(self):
        """ View for editing users. Includes permission handling. """

        form = Form(self.request, schema=UsersEditSchema,
                    state=State(request=self.request))

        search_results = []
        search = u""

        if form.validate():
            search = self.request.params['search']

            # Loop through all the users and create dict of groups
            for user in self.context:
                if search.lower() in self.context[user].username.lower():
                    search_results.append(self.context[user])

            if 'save' in self.request.params.keys() and \
                    self.request.params['save'] == 'Save':
                self.message = msg['saved']
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

        _dict = {
            'page': self.context,
            'form': FormRenderer(form),
            'search_results': search_results,
            'message': self.message,
            'group_names': group_names,
            'has_group': has_group,
            'sorted_gnames': sorted_gnames(),
            'result_count': len(search_results),
            'search_term': search
        }
        return dict(self.base_dict.items() + _dict.items())


class NewsWidget(BaseView):
    """ Widget for news. It's shown in every page inside
    base template"""

    @view_config(context=ISiteRoot, name="news_widget",
            renderer='templates/news_widget.pt')
    def __call__(self):
        news = self.context['news'].order_by_time()
        news_number = 3

        _dict = {
            'news': news[0:news_number],
            'shorten': shorten_text
        }
        return dict(self.base_dict.items() + _dict.items())


class NewsItem(BaseView):
    """ Views for single newsitem """

    @view_config(context=NewsItem, renderer='templates/news_item.pt')
    def __call__(self):
        _dict = {
            'title': self.context.title,
            'text': self.context.text,
            'image_url': self.context.image_url,
        }
        return dict(self.base_dict.items() + _dict.items())

    @view_config(context=NewsItem, name='edit',
            renderer='templates/news_item_edit.pt', permission='edit_content')
    def view_news_item_edit(self):
        form = Form(self.request, schema=NewsCreateSchema,
                state=State(request=self.request))
        title = get_param(self.request, 'title', _return=self.context.title)
        text = get_param(self.request, 'text', _return=self.context.text)
        image_url = get_param(self.request, 'image_url',
                _return=self.context.image_url)

        if form.validate():
            self.context.title = title
            self.context.text = text
            self.context.image_url = image_url
            self.message = msg['saved']

        _dict = {
            'title': title,
            'content': text,
            'image_url': image_url,
            'form': FormRenderer(form),
        }
        return dict(self.base_dict.items() + _dict.items())


class NewsView(BaseView):
    """ View for news which contains all the news """

    @view_config(context=News, renderer='templates/news.pt')
    def __call__(self):
        _dict = {
            'news': self.context,
        }
        return dict(self.base_dict.items() + _dict.items())

    @view_config(context=News, name="create",
                renderer='templates/news_create.pt',
                permission="edit_container")
    def view_news_create(self):
        form = Form(self.request, schema=NewsCreateSchema,
                    state=State(request=self.request))
        title = get_param(self.request, 'title')
        text = get_param(self.request, 'text')
        image_url = get_param(self.request, 'image_url')

        if form.validate():
            item_context = self.context.add(title, text,
                    image_url, self.logged_in)
            return HTTPFound(location=resource_url(item_context,
                    self.request))

        _dict = {
            'page': self.context,
            'context_url': resource_url(self.context, self.request),
            'form': FormRenderer(form),
            'title': title,
            'content': text,
            'image_url': image_url,
        }
        return dict(self.base_dict.items() + _dict.items())

    @view_config(context=News, name="edit",
                renderer='templates/news_edit.pt', permission="edit_container")
    def view_news_edit(self):
        form = Form(self.request, schema=BaseSchema,
                    state=State(request=self.request))
        if form.validate():
            # Filter checkbox-parameters from request
            cbs = [p for p in self.request.params.keys()
                            if u'checkbox' in p]

            # check all the checkbox-parameters and
            # parse them
            for cb in cbs:
                item = self.request.params[cb]
                self.context.remove(item)
                self.message = msg['items_removed']

        _dict = {
            'context_url': resource_url(self.context, self.request),
            'form': FormRenderer(form),
            'message': self.message,
        }
        return dict(self.base_dict.items() + _dict.items())


class EditBarView(BaseView):
    """ View for editor bars. The bar is only
    shown when user with a specific permission tries to
    view content """

    @view_config(context=IContainer, name="editbar",
            renderer='templates/container_editbar.pt')
    def view_container_bar(self):
        """ Bar for container """
        _dict = {
            'edit_url': resource_url(self.context, self.request) + 'edit',
            'create_url': resource_url(self.context, self.request) + 'create',
            'has_permission': has_permission('edit_container',
                            self.context, self.request)
        }
        return dict(self.base_dict.items() + _dict.items())

    @view_config(context=IContent, name="editbar",
            renderer='templates/content_editbar.pt')
    def view_content_bar(self):
        """ Bar for single content """
        _dict = {
            'edit_url': resource_url(self.context, self.request) + 'edit',
            'has_permission': has_permission('edit_content',
                            self.context, self.request)
        }
        return dict(self.base_dict.items() + _dict.items())


class CommentView(BaseView):
    """ View for comments """

    @view_config(context=IComment, name="comments",
            renderer='templates/comments.pt')
    def __call__(self):
        _dict = {
            'comments': self.context.comments
        }
        return dict(self.base_dict.items() + _dict.items())

    @view_config(context=IComment, name="add_comment")
    def add_comment(self):
        _dict = {
            'asdf': 'asdf'
        }
        return dict(self.base_dict.items() + _dict.items())
