import unittest
from easyblog.models import appmaker

from pyramid import testing

class AppMakerTests(unittest.TestCase):
    def test_it(self):
        root = {}
        appmaker(root)
        self.assertEqual(root['app_root']['users']['admin'].username,
                         'admin')
class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        # init request for test cases
        self.dummy_request = testing.DummyRequest()
        self.dummy_request.params['username'] = 'user'
        self.dummy_request.params['password'] = 'password'
        self.dummy_request.params['email'] = 'user@user.com'
        self.dummy_request.params['form.submitted'] = ''

        self.context = appmaker({})

    def tearDown(self):
        testing.tearDown()

    def test_signup(self):
        from easyblog.views import signup
        from easyblog.exceptions import UsernameAlreadyInUseException
        # Adding the user should work
        info = signup(self.context, self.dummy_request)
        self.assertEqual(info['message'], 'Successfully added user: user')
        self.assertEqual(self.context['groups']['user'], ['group:members'])

        # Username should be already in use
        self.assertRaises(UsernameAlreadyInUseException, 
                        signup, self.context,self.dummy_request )

        # Add another user to test user id
        self.dummy_request.params['username'] = 'another_user'
        self.dummy_request.params['password'] = 'another_password'
        signup(self.context, self.dummy_request)
        self.assertEqual(self.context['users'][self.dummy_request.params['username']].id, 3)

    def test_login(self):
        from easyblog.views import login, signup
        from pyramid.httpexceptions import HTTPFound
        signup(self.context, self.dummy_request)
        info = login(self.context, self.dummy_request)
        self.assertEquals(type(info), HTTPFound)

        self.dummy_request.params['username'] = 'another_user'
        self.dummy_request.params['password'] = 'another_password'
        info = login(self.context, self.dummy_request)
        self.assertNotEquals(type(info), HTTPFound)



class ModelTests(unittest.TestCase):
    def test_blogpost(self):
        from easyblog.models import BlogPost
        instance = BlogPost(subject=u'subject', text=u'text', 
                            user=u'id')

        self.assertEqual(instance.subject, u'subject')
        self.assertEqual(instance.text, u'text')
        self.assertEqual(instance.user, u'id')

    def test_password_validation(self):
        from easyblog.models import User
        user = User('user', 'password', 'user@user.com', 1234)
        self.assertEquals(True, user.validate_password('password'))
        self.assertEquals(False, user.validate_password('PaSsword'))

class FunctionalTests(unittest.TestCase):
    admin_login = '/login?username=admin&password=adminpw#' \
                   '&email=admin@admin.com&came_from=Home&form.submitted=Login'

    member_signup = '/signup?username=member&password=memberpw' \
                   '&email=member@member.com&form.submitted=Signup'

    member_login = '/login?username=member&password=memberpw' \
                   '&email=member@member.com&came_from=Home&form.submitted=Login'

    
    second_member_signup = '/signup?username=second_member&password=secondmemberpw' \
                   '&email=second.member@member.com&form.submitted=Login'

    second_member_login = '/login?username=second_member&password=secondmemberpw' \
                   '&email=second.member@member.com&came_from=Home&form.submitted=Login'
    

    def setUp(self):
        # Build testing environment
        import tempfile
        import os.path
        from easyblog import main
        self.tmpdir = tempfile.mkdtemp()

        dbpath = os.path.join( self.tmpdir, 'test.db')
        uri = 'file://' + dbpath
        settings = { 'zodbconn.uri' : uri ,
                     'pyramid.includes': ['pyramid_zodbconn', 'pyramid_tm'] }

        app = main({}, **settings)
        self.db = app.registry.zodb_database
        from webtest import TestApp
        self.testapp = TestApp(app)

        # init two test users, admin is already defined
        self.testapp.get(self.member_signup)
        self.testapp.get(self.second_member_signup)

    def test_user_edit_without_loggin_in(self):
        res = self.testapp.get('/users/admin/edit', status=200)
        self.assertTrue('Login' in res.body)
        res = self.testapp.get('/users/member/edit', status=200)
        self.assertTrue('Login' in res.body)
        res = self.testapp.get('/users/second_member/edit', status=200)
        self.assertTrue('Login' in res.body)

    def test_logout_page(self):
        res = self.testapp.get(self.admin_login, status=200)
        res = self.testapp.get('/logout', status=302)
        self.assertEquals(res.location, 'http://localhost/')

    def test_logout_link_present_after_login(self):
        pass
    
    def test_login_link_present_after_logout(self):
        pass

    def test_user_edit(self):
        #login as member
        res = self.testapp.post(self.member_login)
        res = self.testapp.get('/users/member/edit', status=200)
        self.assertTrue('member' in res.body.lower())
    
        # after logout, edit should show login window
        self.testapp.get('/logout')
        res = self.testapp.get('/users/member/edit', status=200)
        self.assertTrue('Login' in res.body)

    def test_forbidden_user_to_admin_edit(self):
        #login as member
        res = self.testapp.post(self.member_login)

        # try to access admin edit-view (should fail)
        res = self.testapp.get('/users/second_member/edit', status=403)
        self.assertEquals(res.status, '403 Forbidden')

        # admin has the permission "edit_all" so it should be able to access
        # the content
        res = self.testapp.post('/logout')
        res = self.testapp.post(self.admin_login)
        res = self.testapp.get('/users/second_member/edit', status=200)
        self.assertTrue('second_member' in res.body)


    def test_logout_link_when_logged_in(self):
        res = self.testapp.post(self.member_login)
        res = self.testapp.get('/', status=200)
        self.assertTrue('Logout' in res.body)

    def test_logout_link_not_present_after_logged_out(self):
        res = self.testapp.get('/', status=200)
        self.assertFalse('Logout' in res.body)

    def test_member_email_change(self):
        pass

    def test_email_validation(self):
        pass


    def test_member_access_denied_to_different_user(self):
        pass
        
        
