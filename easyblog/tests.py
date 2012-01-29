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

        request = testing.DummyRequest(post=multidict, params=NestedMultiDict(multidict))
        request.session = Mock()
        csrf_token = Mock()
        csrf_token.return_value = csrf

        request.session.get_csrf_token = csrf_token
        request.root = self.zodb
        return request

    def tearDown(self):
        testing.tearDown()

    def test_users_edit_view_search(self):
        from easyblog.views import view_users_edit
        request = self.get_csrf_request(post={
            u'submit': u'Search',
            u'search': u'adm'
        })
        context = self.zodb['users']
        result = view_users_edit(context, request)
        self.assertEqual(1, len(result['search_results']))

    def test_users_edit_view_add_permission(self):
        from easyblog.views import view_users_edit
        from easyblog.security import group_names
        request = self.get_csrf_request(post={
            u'submit': u'Save',
            u'search': u'adm',
            u'checkbox:admin': group_names['admin'],
            u'checkbox:admin': group_names['member']
        })
        context = self.zodb['users']
        view_users_edit(context, request)
        self.assertTrue(group_names['member'] in self.zodb['groups']['admin'])


class ModelTests(unittest.TestCase):
    def test_blogpost(self):
        from easyblog.models import BlogPost
        instance = BlogPost(subject=u'subject', text=u'text',
                username=u'admin')

        self.assertEqual(instance.subject, u'subject')
        self.assertEqual(instance.text, u'text')
        self.assertEqual(instance.username, u'admin')

    def test_password_validation(self):
        from easyblog.models import User
        user = User('user', 'password', 'user@user.com', 1234)
        self.assertNotEquals('password', user.password)
        self.assertEquals(True, user.validate_password('password'))
        self.assertEquals(False, user.validate_password('PaSsword'))

    def test_user_edit(self):
        from easyblog.models import User
        user = User('user', 'password', 'user@user.com', 1234)
        tmp_pw = user.password
        user.edit('password2', 'user@user.com')
        self.assertNotEquals('password2', user.password)
        self.assertNotEquals(tmp_pw, user.password)

    def test_set_group(self):
        pass

    def test_has_blogname(self):
        from easyblog.models import Blogs
        blogs = Blogs()
        blogs.add(u'test test', u'admin')
        self.assertTrue(blogs.has_blog(u'test test'))

    def test_blog_timestamp(self):
        from easyblog.models import Blog
        blog = Blog(u'My Blog', u'member', 1)
        blog.add(u'subject', u'here is some text', 'member')
        for key in blog:
            self.assertTrue(blog[key].timestamp != "")

    def test_blog_post_add(self):
        from easyblog.models import Blog
        blog = Blog(u'My Blog', u'member', 1)
        blog.add(u'subject', u'here is some text', 'member')
        for key in blog:
            import hashlib
            m = hashlib.md5()
            m.update(blog[key].username)
            m.update(blog[key].timestamp.isoformat())
            test_id = m.digest()
            self.assertEquals(blog[key].id, test_id)


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

    def _create_blog(self, res,  blogname):
        form = res.forms[0]
        form['blogname'] = blogname
        return form.submit()

    def _add_post(self, res, subject, text):
        form = res.forms[0]
        form['subject'] = subject
        form['text'] = text
        return form.submit()

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
        self.assertTrue('Password is invalid' in res.body)

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

    def test_blogs_page(self):
        res = self.testapp.get('/blogs')
        self.assertTrue('List of blogs' in res.body)

    def test_blog_create(self):
        res = self._login('member', 'memberpw#')
        res = self.testapp.get('/blogs/create')
        self.assertTrue('Login' in res.body)

        res = self._login('admin', 'adminpw#')
        res = self.testapp.get('/blogs/create')
        self.assertTrue('Create Blog' in res.body)

        res = self._create_blog(res, 'My Blog')
        self.assertTrue('List of blogs' in res.body or
                        'should be redirected' in res.body)
        res = self.testapp.get(urllib.quote('/blogs/b0'))
        self.assertTrue('My Blog' in res.body)

    def test_blog_edit(self):
        # login as member and create a new blog
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get('/blogs/create')
        self._create_blog(res, 'My Blog')

        # logout and test permission
        res = self.testapp.get('/logout')
        res = self.testapp.get(urllib.quote('/blogs/b0/edit'))
        self.assertTrue('Username' in res.body)

        # login as admin and test permission
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get(urllib.quote('/blogs/b0/edit'))
        self.assertTrue('Edit My Blog' in res.body)

    def test_blog_add_post(self):
        # login as member and create a new blog
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get('/blogs/create')
        self._create_blog(res, 'myblogi')
        res = self.testapp.get('/blogs/b0/add_post')
        self._add_post(res, u'thisisasubject',
                    'Here is some text for testing.')
        res = self.testapp.get('/blogs/b0')
        self.assertTrue('thisisasubject' in res.body)
        self.assertTrue('admin wrote' in res.body)

        # Test single
        res = self.testapp.get('/blogs/b0/p0')

    def test_blog_remove(self):
        # Login as admin and create blog
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get('/blogs/create')
        self._create_blog(res, 'myblogi')

        res = self.testapp.get('/blogs/b0/remove')
        # Press Remove button
        form = res.forms[0]
        res = form.submit()
        self.assertTrue('List of blogs' in res.body or
                        'should be redirected' in res.body)

    def test_admin_view(self):
        res = self.testapp.get('/users/edit')
        self.assertTrue('Login' in res.body and 'username' in res.body.lower())

        # Login as admin and go admin view
        res = self._login('admin', 'adminpw#')
        res = self.testapp.get('/users/edit')
        self.assertTrue('Edit users' in res.body)
