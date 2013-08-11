# -*- coding: utf-8 -*-
import unittest

from easyblog.models import appmaker
from mock import Mock

import urllib
from pyramid import testing


class AppMakerTests(unittest.TestCase):
    def test_it(self):
        root = {}
        appmaker(root)
        self.assertEqual(root['app_root']['users']['admin'].username,
                         'admin')
        self.assertTrue(root['app_root']['blogs'].__name__)

    def test_has_special_method(self):
        from easyblog.utilities import has_special
        self.assertTrue(has_special("testi%$|") != None)
        self.assertEqual(has_special("testi"), None)

class UtilitiesTests(unittest.TestCase):
    def test_list_splitting(self):
        from .utilities import chunks
        test_list = ['test', 'test2', 'test3',
                'test4', 'test5', 'test6', 'test7',
                'test8', 'test9', 'test10']

        split = chunks(test_list, 3)
        self.assertTrue(4, len(split))


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        # init request for test cases
        self.dummy_request = testing.DummyRequest()
        self.dummy_request.params['username'] = 'user'
        self.dummy_request.params['password'] = 'password'
        self.dummy_request.params['email'] = 'user@user.com'
        self.dummy_request.params['submit'] = 'Submit'

        self.zodb = appmaker({})

    def get_csrf_request(self, post=None):
        csrf = 'abc'

        if not u'_csrf' in post.keys():
            post.update({
                '_csrf': csrf
            })

        # We can't use dummyrequest cause the simpleform
        # needs MultiDict and NestedMultiDict from WebOb request
        # This is the 'real' request.
        from webob.multidict import MultiDict, NestedMultiDict
        multidict = MultiDict()
        # This is my own invention. Use with caution :)
        # request = Request.blank('/', method="POST", registry=registry)

        for key in post.keys():
            multidict[key] = post[key]

        request = testing.DummyRequest(post=multidict,
                params=NestedMultiDict(multidict))
        request.session = Mock()
        csrf_token = Mock()
        csrf_token.return_value = csrf

        request.session.get_csrf_token = csrf_token
        request.root = self.zodb
        return request

    def tearDown(self):
        testing.tearDown()

    def test_users_edit_view_search(self):
        from easyblog.views import UsersView
        request = self.get_csrf_request(post={
            u'submit': u'Search',
            u'search': u'adm'
        })
        context = self.zodb['users']
        view = UsersView(context, request)
        result = view.view_users_edit()
        self.assertEqual(1, len(result['search_results']))

    def test_users_edit_view_add_permission(self):
        from easyblog.views import UsersView
        from easyblog.security import group_names
        request = self.get_csrf_request(post={
            u'save': u'Save',
            u'search': u'adm',
            u'checkbox:admin': group_names['admin'],
            u'checkbox:admin': group_names['member']
        })
        context = self.zodb['users']
        view = UsersView(context, request)
        view.view_users_edit()
        self.assertTrue(group_names['member'] in self.zodb['groups']['admin'])

    def test_news_add_item(self):
        from easyblog.views import NewsView
        request = self.get_csrf_request(post={
            u'submit': u'Create',
            u'title': u'We\'re gonna celebrate soon!',
            u'text': u'Bowmore whiskey is the best, that\'s why we\'re gonna \
                    celebrate soon',
            u'image_url': u'http://www.google.com'
        })
        view = NewsView(self.zodb['news'], request)
        view.view_news_create()
        self.assertTrue('gonna celebrate' in self.zodb['news']['n0'].title)


class ModelTests(unittest.TestCase):
    def test_blogpost(self):
        from easyblog.models import BlogPost
        instance = BlogPost(title=u'subject', text=u'text',
                owner=u'admin', id='p0')

        self.assertEqual(instance.title, u'subject')
        self.assertEqual(instance.text, u'text')
        self.assertEqual(instance.owner, u'admin')

    def test_password_validation(self):
        from easyblog.models import User
        user = User('user', 'password', 'user@user.com')
        self.assertNotEquals('password', user.password)
        self.assertEquals(True, user.validate_password('password'))
        self.assertEquals(False, user.validate_password('PaSsword'))

    def test_user_add(self):
        from easyblog.models import Users
        users = Users(u'users', u'main', u'users')
        users.add('user', 'password', 'user@user.com')
        users.add('admin', 'password', 'admin@user.com')
        self.assertTrue(users.has_user('user'))
        self.assertFalse(users.has_user('user2'))

    def test_user_edit(self):
        from easyblog.models import User
        user = User('user', 'password', 'user@user.com')
        tmp_pw = user.password
        user.edit('password2', 'user@user.com')
        self.assertNotEquals('password2', user.password)
        self.assertNotEquals(tmp_pw, user.password)

    def test_group_remove_group(self):
        from easyblog.models import Groups
        groups = Groups(u'groups', u'main', u'groups')
        groups.add(u'admin', u'group:admins')
        groups.add(u'member', u'group:members')
        groups.add(u'editor', u'group:editors')
        groups.remove_group(u'member', u'group:members')
        self.assertTrue(groups['member'] == [])

    def test_group_policy_add(self):
        from easyblog.models import Groups
        groups = Groups(u'groups', u'main', u'groups')
        policy = {u'admin': [u'group:admins', u'group:editors'],
                  u'member': [u'group:members', u'group:editors']}
        groups.add_policy(policy)
        self.assertEqual(len(groups[u'member']), 3)

    def test_has_blogname(self):
        from .models import Blogs
        blogs = Blogs(u'blogs', u'main', u'blogs')
        blogs.add(u'test test', u'description for our beautiful blog',
                u'http://google.com', u'admin')
        self.assertTrue(blogs.has_blog(u'test test'))
        self.assertFalse(blogs.has_blog(u'afsdfas'))

    def test_groups_flusj(self):
        from .models import Groups
        groups = Groups(u'groups', u'main', u'groups')
        groups.add(u'member', u'members:group')
        groups.flush(u'member')
        self.assertTrue(groups[u'member'] == [])

    def test_blog_timestamp(self):
        from easyblog.models import Blog
        blog = Blog(u'My Blog', u'Here is some text for blog',
                'http://google.com', u'member', 1)
        blog.add(u'subject', u'here is some text', 'member')
        for key in blog:
            self.assertTrue(blog[key].timestamp != "")

    def test_blogpost_create(self):
        from easyblog.models import Blog
        blog = Blog(u'My Blog', u'Description for our blog',
                u'http://google.com', u'member', 1)
        blog.add(u'subject', u'here is some text', 'member')
        self.assertEquals(blog['p0'].id, 'p0')

    def test_news_add(self):
        from easyblog.models import News
        news = News(u'news', u'main', u'news')
        news.add(u'Title for news', u'Here we write some content for the news',
                 u'', u'admin')
        self.assertTrue(news.has_item(u'Title for news'))

    def test_news_by_owner(self):
        from easyblog.models import News
        news = News(u'news', u'main', u'news')
        news.add(u'Title for news', u'Here we write some content for the news',
                 u'', u'admin')
        news.add(u'Title for news4', u'Here we write some content \
                for thsadfas fe news',
                 u'', u'admin')
        news.add(u'Latest news_item', u'dfasasdfHere we write some \
                content for the news',
                 u'', u'member')
        self.assertEqual(len(news.items_by_owner('admin')), 2)
        return news

    def test_news_ordering(self):
        news = self.test_news_by_owner()
        _list = news.order_by_time()
        self.assertEqual(_list[0].title, u'Latest news_item')

    def test_blogs_by_owner(self):
        pass

    def test_blogs_ordering(self):
        pass

class FunctionalTests(unittest.TestCase):
    admin_login = '/login?username=admin&password=adminpw#' \
                   '&email=admin@admin.com&came_from=Home&submit=Submit'

    member_signup = '/signup?username=member&password=memberpw' \
                    '&confirm_password=memberpw' \
                   '&email=member@member.com&submit=Submit'

    member_login = '/login?username=member&password=memberpw' \
                   '&email=member@member.com&came_from=Home&submit=Submit'

    second_member_signup = '/signup?username=second_member' \
                    '&password=secondmemberpw' \
                   '&email=second.member@member.com&submit=Submit'

    second_member_login = '/login?username=second_member' \
                    '&password=secondmemberpw' \
                   '&email=second.member@member.com&submit=Submit'

    def _signup(self, username, password, password_confirm, email):
        res = self.testapp.get('/signup')
        form = res.forms[0]
        form['username'] = username
        form['password'] = password
        form['password_confirm'] = password_confirm
        form['email'] = email
        return form.submit()

    def _login(self, username, password):
        res = self.testapp.get('/login')
        form = res.forms[0]
        form['username'] = username
        form['password'] = password
        return form.submit()

    def _edit_user(self, res, password,
                    new_password, new_password_confirm, email):
        form = res.forms[0]
        form['password'] = password
        form['new_password'] = new_password
        form['new_password_confirm'] = new_password_confirm
        form['email'] = email
        return form.submit()
    
    def _edit_page(self, res, title, text):
        form = res.forms[0]
        form['title']  = title
        form['text'].value  = text
        return form.submit()

    def _create_blog(self, res,  blogname, description, image_url=u""):
        form = res.forms[0]
        form['blogname'] = blogname
        form['text'] = description
        form['image_url'] = image_url
        return form.submit()

    def _create_news(self, res, title, text, image_url):
        form = res.forms[0]
        form['title'] = title
        form['text'] = text
        form['image_url'] = image_url
        return form.submit()

    def _create_post(self, res, title, text):
        form = res.forms[0]
        form['title'] = title
        form['text'] = text
        return form.submit()

    def _search_user(self, res, user):
        form = res.forms[0]
        form['search'] = user
        return form.submit("submit")

    def _create_second_editor(self):
        res = self.testapp.get('/logout')
        self._signup('editor2', 'editor2pw#',
                    'editor2pw#', 'editor2@editor.com')

        # Make second editor
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get('/users/edit')
        res = self._search_user(res, 'editor2')

        # fill remove editor permission
        form = res.forms[0]
        form.set('checkbox-editor:editor2', True)
        res = form.submit("save")
        self.testapp.get('/logout')

    def setUp(self):
        # Build testing environment
        import tempfile
        import os.path
        from easyblog import main
        self.tmpdir = tempfile.mkdtemp()

        dbpath = os.path.join(self.tmpdir, 'test.db')
        uri = 'file://' + dbpath
        settings = {'zodbconn.uri': uri,
                     'pyramid.includes': ['pyramid_zodbconn', 'pyramid_tm']}

        app = main({}, **settings)
        self.db = app.registry.zodb_database
        from webtest import TestApp
        self.testapp = TestApp(app)

        # init two test users, admin is already defined
        self._signup('member', 'memberpw#', 'memberpw#', 'member@member.com')
        self._signup('second_member', 'second_memberpw#',
                    'second_memberpw#', 'second_member@member.com')
        self.testapp.get('/lang-en')

    def tearDown(self):
        import shutil
        self.db.close()
        shutil.rmtree(self.tmpdir)

    def test_user_edit_without_loggin_in(self):
        res = self.testapp.get('/users/admin/edit', status=200)
        self.assertTrue('Login' in res.body)
        res = self.testapp.get('/users/member/edit', status=200)
        self.assertTrue('Login' in res.body)
        res = self.testapp.get('/users/second_member/edit', status=200)
        self.assertTrue('Login' in res.body)

    def test_signup_username_already_in_use(self):
        res = self._signup('member', 'memberpw#', 'memberpw#',
                           'member@member.com')
        self.assertTrue('already exists' in res.body)

    def test_signup_username_special_characters(self):
        res = self._signup('member{}', 'memberpw#2l', 'memberpw#2l',
                           'member@member.comas')
        self.assertTrue('special' in res.body)

    def test_logout_page(self):
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get('/logout', status=302)
        self.assertEquals(res.location, 'http://localhost/')

    def test_user_edit(self):
        #login as member
        res = self._login('member', 'memberpw#')
        res = self.testapp.get('/users/member/edit', status=200)
        self.assertTrue('member' in res.body.lower())
        self.assertFalse('Login' in res.body)

        res = self.testapp.get('/users/second_member/edit', status=200)
        self.assertTrue('Login' in res.body)

        # after logout, edit should show login window
        self.testapp.get('/logout')
        res = self.testapp.get('/users/member/edit', status=200)
        self.assertTrue('Login' in res.body)

    def test_forbidden_user_to_admin_edit(self):
        #login as member
        res = self._login('member', 'memberpw#')

        # should return 200 ok for normal view
        res = self.testapp.get('/users/member', status=200)
        self.assertEquals(res.status, '200 OK')

        # try to access admin edit-view (should fail)
        res = self.testapp.get('/users/second_member/edit')
        self.assertTrue('Username' in res.body)

        # admin has the permission "edit_all" so it should be able to access
        # the content
        res = self.testapp.get('/logout')
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get('/users/second_member/edit', status=200)
        self.assertTrue('second_member' in res.body)

    # TODO: TEST IT
    def test_password_change(self):
        pass

    def test_logout_link_when_logged_in(self):
        res = self._login('member', 'memberpw#')
        res = self.testapp.get('/', status=200)
        self.assertTrue('Logout' in res.body)

    def test_logout_link_not_present_after_logged_out(self):
        res = self.testapp.get('/', status=200)
        self.assertFalse('Logout' in res.body)

    def test_member_email_edit(self):
        res = self._login('member', 'memberpw#')
        res = self.testapp.get('/users/member/edit')

        # Try to change with invalid password, should fail
        res = self._edit_user(res, 'member', 'memberpw#2',
                            'memberpw#2', 'member@changed.com')
        self.assertTrue('Invalid Password' in res.body)

        # Try to change with incorrect email and password confirm, should fail
        res = self._edit_user(res, 'memberpw#', 'memberpw#2',
                              'memberpw#asd2', 'member@')
        self.assertTrue('do not match' in res.body)
        self.assertTrue('email address is invalid' in res.body)

        res = self._edit_user(res, 'memberpw#', 'memberpw#2',
                              'memberpw#2', 'member@changed.com')
        #TODO: NAME RIGHT
        self.assertTrue('Successfully saved' in res.body)

    def test_email_and_pw_validation(self):
        res = self._signup('emailfail', 'emailfailpw',
                           'emailfailpw23', 'fail@')
        self.assertTrue('do not match' in res.body)
        self.assertTrue('email address is invalid' in res.body)

    def test_username_already_in_use(self):
        res = self._signup('member', 'memberpw', 'memberpw',
                           'member@member.com')
        self.assertTrue('already exists' in res.body)

    def test_blog_create(self):
        res = self._login('member', 'memberpw#')
        res = self.testapp.get('/blogs/create')
        self.assertTrue('Login' in res.body)

        res = self._login('editor', 'editorpw#')
        res = self.testapp.get('/blogs/create')
        self.assertTrue('Create Blog' in res.body)

        res = self._create_blog(res, u'My Blog', u'This is my blog',
                u'')
        self.assertTrue('List of blogs' in res.body or
                        'should be redirected' in res.body)
        res = self.testapp.get('/blogs')
        self.assertTrue('My Blog' in res.body)

    def test_blog_edit_permission(self):
        self.test_blog_create()
        res = self.testapp.get('/blogs/b0/edit')
        self.assertTrue('This is my blog' in res.body)

    def test_blog_edit(self):
        # login as member and create a new blog
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get('/blogs/create')
        self._create_blog(res, 'My Blog', u'This is my blog',
                u'http://google.com')

        # logout and test permission
        res = self.testapp.get('/logout')
        res = self.testapp.get(urllib.quote('/blogs/b0/edit'))
        self.assertTrue('Username' in res.body)

        # login as admin and test permission
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get(urllib.quote('/blogs/b0/edit'))
        self.assertTrue("My Blog" in res.body)

    def test_blogpost_edit(self):
        self.test_blogpost_create()
        res = self.testapp.get('/blogs/b0/p0/edit')
        self._create_post(res, 'title changed', 'content changed fully')
        res = self.testapp.get('/blogs/b0/p0/')
        self.assertTrue('title changed' in res.body)
        self.assertTrue('content changed fully' in res.body)

    def test_blog_edit_blogposts(self):
        self.test_blogpost_create()
        res = self.testapp.get('/blogs/b0/edit')
        self.assertTrue('thisisasubject' in res.body)
        self.assertTrue('table' in res.body)

    def test_blogpost_edit_link(self):
        self.test_blogpost_create()
        res = self.testapp.get('/blogs/b0/p0')
        self.assertTrue('Edit' in res.body)

    def test_blogpost_create(self):
        res = self._login('editor', 'editorpw#')
        res = self.testapp.get('/blogs/create')
        self._create_blog(res, 'myblogi' , u'Description for blogs',
                u'http://google.com')
        res = self.testapp.get('/blogs/b0/create')
        self._create_post(res, u'thisisasubject',
                    'Here is some text for testing.')
        res = self.testapp.get('/blogs/b0')
        self.assertTrue('thisisasubject' in res.body)

        res = self.testapp.get('/blogs/b0/p0')
        self.assertTrue('thisisasubject' in res.body)

    def test_blog_editbar(self):
        self.test_blogpost_create()
        #TODO 

    # TODO: Do we want every editor to edit blogs?
    # def test_blogs_edit_permission(self):
    #     self.test_blogpost_create()
    #     res = self.testapp.get('/blogs/b0/edit')
    #     self.assertTrue('alert-error' in res.body)
    #     res = self._login('admin', 'adminpw#')
    #     res = self.testapp.get('/blogs/b0/edit')
    #     self.assertTrue('checkbox' in res.body)

    def test_blogpost_edit_permission(self):
        self.test_blogpost_create()
        self._create_second_editor()
        self._login(u'editor2', u'editor2pw#')
        res = self.testapp.get('/blogs/b0/p0/edit')
        self.assertTrue('alert-error' in res.body)

   
    # TODO: is this needed?
    # def test_blog_action_button(self):
    #     self.test_blogpost_create()
    #     res = self.testapp.get('/blogs/b0/')
    #     self.assertTrue('Edit' in res.body)
    #     self._create_second_editor()
    #     self._login('editor2', 'editor2pw#')
    #     res = self.testapp.get('/blogs/b0/')
    #     self.assertFalse('Edit' in res.body)


    def test_blogpost_owner(self):
        self.test_blogpost_edit_permission()
        res = self.testapp.get('/blogs/b0/p0/')
        self.assertFalse('Edit' in res.body)

    def test_blog_owner(self):
        self.test_blog_create()
        self._create_second_editor()
        self._login('editor2', 'editor2pw#')
        res = self.testapp.get('/blogs/b0/edit')
        self.assertTrue('alert-error' in res.body)

    def test_blog_remove(self):
        # Login as admin and create blog
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get('/blogs/create')
        self._create_blog(res, 'myblogi', 'here is some description for myblogi',
                'http://google.com')

        res = self.testapp.get('/blogs/b0/remove')
        # Press Remove button
        form = res.forms[0]
        res = form.submit()
        self.assertTrue('List of blogs' in res.body or
                        'should be redirected' in res.body)

    def test_admin_view(self):
        res = self._login('editor', 'editorpw#')
        res = self.testapp.get('/users/edit')
        self.assertTrue('review this content' in res.body and
                'username' in res.body.lower())

        # Login as admin and go admin view
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get('/users/edit')
        self.assertTrue('Edit users' in res.body)

    def test_users_edit_permission_change(self):
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get('/users/edit')
        res = self._search_user(res, 'editor')

        # fill remove editor permission
        form = res.forms[0]
        form.set('checkbox-editor:editor', False, 0)
        res = form.submit("save")
        self._login('editor', 'editorpw#')
        res = self.testapp.get('/blogs/create')
        self.assertTrue('Username' in res.body)

    def test_users_edit(self):
        # login as admin
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get('/users/edit')

        # Use search form to look for 'member' user
        form = res.forms[0]
        form['search'] = 'memb'
        res = form.submit('submit')
        self.assertTrue('member' in res.body)

    def test_news_view(self):
        res = self.testapp.get('/news')
        self.assertTrue('List of News' in res.body)

    def test_news_create(self):
        res = self._login('editor', 'editorpw#')
        res = self.testapp.get('/news/create')
        self.assertTrue('Create a single news item' in res.body)
        res = self._create_news(res, 'Title for our news',
                        'Here is some text for the news',
                        'http://google.com')
        self.assertTrue('Title for our news' or
                        'should be redirected' in res.body)

        res = self.testapp.get('/')
        self.assertTrue('Title for our news' in res.body)

    def test_news_item_edit(self):
        # create an item
        self.test_news_create()
        res = self.testapp.get('/news/n0/edit')
        self.assertTrue('Title' in res.body)

        # try to edit with incorrect information
        res = self._create_news(res, u'',
                        u'Here is some text for the news',
                        u'http://google.com')
        self.assertTrue('alert-error' in res.body)

        # then just update with correct information
        res = self._create_news(res, u'Changed title',
                        u'Here is some text for the news',
                        u'http://google.com')
        res = self.testapp.get('/news/n0')
        self.assertTrue('Changed title' in res.body)

    def test_newsitem_edit_link(self):
        self.test_news_create()
        res = self.testapp.get('/news/n0/')
        self.assertTrue('Edit' in res.body)

    def test_news_owner(self):
        self.test_news_create()
        self._create_second_editor()
        self._login('editor2', 'editor2pw#')
        res = self.testapp.get('/news/n0/')
        self.assertTrue('Edit' in res.body)

    def test_news_create_link(self):
        # Login as member, there shouldn't be
        # create link
        res = self._login('member', 'memberpw#')
        res = self.testapp.get('/news')
        self.assertFalse('Edit' in res.body)

        # Editor should see it
        res = self._login('editor', 'editorpw#')
        res = self.testapp.get('/news')
        self.assertTrue('Edit' in res.body)

    def test_blogs_create_link(self):
        # Login as member, there shouldn't be
        # create link
        res = self._login('member', 'memberpw#')
        res = self.testapp.get('/blogs')
        self.assertFalse('Edit' in res.body)

        # Editor should see it
        res = self._login('editor', 'editorpw#')
        res = self.testapp.get('/blogs')
        self.assertTrue('Edit' in res.body)

    def test_news_edit_link(self):
        # Login as member, there shouldn't be
        # create link
        res = self._login('editor', 'editorpw#')
        res = self.testapp.get('/news/edit')
        self.assertTrue('table' in res.body)

    def test_blogs_edit_link(self):
        # Login as member, there shouldn't be
        # create link
        res = self._login('editor', 'editorpw#')
        res = self.testapp.get('/blogs/edit')
        self.assertTrue('table' in res.body)
        res = self._login('member', 'memberpw#')
        res = self.testapp.get('/blogs/edit')
        self.assertTrue('Username' in res.body)

    def test_news_remove(self):
        self.test_news_create()
        res = self.testapp.get('/news/create')
        res = self._create_news(res, 'Title for another news',
                        'Here is some text for the news',
                        'http://google.com')
        res = self.testapp.get('/news/edit')
        form = res.forms[0]
        form.set('checkbox-n0', True, 0)
        res = form.submit()
        self.assertFalse('Title for our news' in res.body)

    def test_blogs_remove(self):
        # Editor shouldn't be allowed to edit blogs
        self.test_blog_create()
        res = self.testapp.get('/blogs/edit')
        self.assertFalse('checkbox' in res.body)
       
        # Admin should
        self._login('admin', 'adminpw#')
        res = self.testapp.get('/blogs/edit')
        form = res.forms[0]
        form.set('checkbox-b0', True, 0)
        res = form.submit()
        self.assertFalse('My Blog' in res.body)

    def test_news_widget(self):
        self.test_news_create()
        res = self.testapp.get('/')
        self.assertTrue('Title for our news' in res.body)

    def test_blogs_view(self):
        res = self.testapp.get('/blogs/')
        self.assertTrue('List of Blogs' in res.body)

    # Page tests
    def test_page_contact_link(self):
        res = self.testapp.get('/contact')
        self.assertTrue('200 OK' in res.status)

    def test_page_about_link(self):
        res = self.testapp.get('/about')
        self.assertTrue('200 OK' in res.status)

    def test_page_about_edit_link(self):
        res = self.testapp.get('/contact/edit')
        self.assertTrue('200 OK' in res.status)

    def test_page_contact_edit_link(self):
        res = self.testapp.get('/contact/edit')
        self.assertTrue('200 OK' in res.status)
    
    def test_page_contact_edit(self):
        self._login('admin', 'adminpw#')
        res = self.testapp.get('/contact/edit')
        self._edit_page(res, 'title',  'test content content content')
        res = self.testapp.get('/contact')
        self.assertTrue('test content' in res.body)
        self.assertTrue('title' in res.body)

    def test_admin_links(self):
        self._login('admin', 'adminpw#')
        res = self.testapp.get('/')
        self.assertTrue('Manage Users' in res.body)
        self.assertTrue('Create User' in res.body)





    # TODO: Test spam bot protection by using a field which is hidden
    # in css 'display: none;'. Spam bot fills the field but users don't.
    # Yes users can use firebug but so what, this covers most of the cases
    def test_spam_bot_protection(self):
        """docstring for test_spam_bot_protection"""
        pass
