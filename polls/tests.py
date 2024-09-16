"""Contain tests."""
from json import dumps, loads
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.http import HttpRequest
from django.contrib.auth.models import User
from polls.views import BasicView
from polls.models import Poll


def get_test_user() -> User:
    """Create a test user."""
    user = User.objects.all().first()
    if user is not None:
        return user
    user = User.objects.create(username="user", password="1234")
    user.set_password("1234")
    return user


class PollTest(TestCase):
    """Test Poll methods."""

    def test_is_published_future(self):
        """Check `is_published` for future polls."""
        pub_date = timezone.now() + timedelta(days=5)
        poll = Poll.objects.create(name="Test Poll",
                                   creator=get_test_user(),
                                   allow=0,
                                   res=0,
                                   image="",
                                   yaml="Test Data",
                                   pub_date=pub_date)
        self.assertFalse(poll.is_published())

    def test_is_published_now(self):
        """Check `is_published` for current polls."""
        poll = Poll.objects.create(name="Test Poll",
                                   creator=get_test_user(),
                                   allow=0,
                                   res=0,
                                   image="",
                                   yaml="Test Data")
        self.assertTrue(poll.is_published())

    def test_is_published_past(self):
        """Check `is_published` for past polls."""
        pub_date = timezone.now() - timedelta(days=5)
        poll = Poll.objects.create(name="Test Poll",
                                   creator=get_test_user(),
                                   allow=0,
                                   res=0,
                                   image="",
                                   yaml="Test Data",
                                   pub_date=pub_date)
        self.assertTrue(poll.is_published())

    def test_can_vote_future(self):
        """Check `can_vote` for future polls."""
        pub_date = timezone.now() + timedelta(days=5)
        poll = Poll.objects.create(name="Test Poll",
                                   creator=get_test_user(),
                                   allow=0,
                                   res=0,
                                   image="",
                                   yaml="Test Data",
                                   pub_date=pub_date)
        self.assertFalse(poll.can_vote(None))

    def test_can_vote_current(self):
        """Check `can_vote` for current polls."""
        pub_date = timezone.now()
        poll = Poll.objects.create(name="Test Poll",
                                   creator=get_test_user(),
                                   allow=0,
                                   res=0,
                                   image="",
                                   yaml="Test Data",
                                   pub_date=pub_date)
        self.assertTrue(poll.can_vote(None))

    def test_can_vote_closed(self):
        """Check `can_vote` for closed polls."""
        pub_date = timezone.now() - timedelta(days=5)
        poll = Poll.objects.create(name="Test Poll",
                                   creator=get_test_user(),
                                   allow=0,
                                   res=0,
                                   image="",
                                   yaml="Test Data",
                                   end_date=timezone.now() - timedelta(days=2),
                                   pub_date=pub_date)
        self.assertFalse(poll.can_vote(None))


class APITest(TestCase):
    """Implement tests for gyatt."""

    # to store session cookie
    cookies = None

    @classmethod
    def _rollback_atomics(cls, atomics):
        """Override the rollback function.

        To stop the rollback of the database for every test.
        """
        return

    def test_a_create_account(self):
        """Create user."""
        response = self.client.post("/register",
                                    data={
                                        "username": "user",
                                        "password1": "1234",
                                        "password2": "1234"
                                    })
        self.assertEqual(response.status_code, 302)
        response = self.client.post("/register",
                                    data={
                                        "username": "user2",
                                        "password1": "1234",
                                        "password2": "1234"
                                    })
        self.assertEqual(response.status_code, 302)

    def test_b_login_account(self):
        """Login as user."""
        response = self.client.post("/accounts/login/",
                                    data={
                                        "username": "user",
                                        "password": "1234"
                                    })
        self.__class__.cookies = response.cookies
        self.assertEqual(response.status_code, 302)

    def test_c_create_poll_no_auth(self):
        """Attempt to create a poll without authentication."""
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "create",
                                        "n": "New Poll",
                                        "i": "https://localhost:80/logo.png",
                                        "a": 2,
                                        "r": 2,
                                        "b": 0,
                                        "y": "yml_data here"
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_d_create_poll(self):
        """Create a poll."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "create",
                                        "n": "New Poll",
                                        "i": "https://localhost:80/logo.png",
                                        "a": 2,
                                        "r": 2,
                                        "b": 0,
                                        "y": "yml_data here"
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        poll = Poll.objects.get(id=1)
        self.assertEqual(poll.name, "New Poll")
        self.assertEqual(poll.image, "https://localhost:80/logo.png")

    def test_e_get_poll(self):
        """Get a poll."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "get",
                                        "n": "1",
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = loads(response.content)
        self.assertEqual(data.get("yaml"), "yml_data here")

    def test_f_not_already_answered(self):
        """Check if the poll already is answered, should be False."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "aa",
                                        "n": "1",
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"n")

    def test_f_submit(self):
        """Submit the poll response."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "submit",
                                        "n": "1",
                                        "r": {
                                            "test_key": "test_val"
                                        }
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")

    def test_g_resubmit(self):
        """Resubmit the poll response."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "submit",
                                        "n": "1",
                                        "r": {
                                            "test_key2": "test_val2"
                                        }
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")

    def test_h_res(self):
        """View the poll response."""
        self.client.cookies = self.__class__.cookies
        poll = Poll.objects.get(id=1)
        data = poll.get_responses()
        self.assertIsNone(data.get("test_key"))
        self.assertIsNotNone(data.get("test_key2"))
        self.assertEqual(data.get("test_key2")[0].get("value"), "test_val2")
        self.assertEqual(data.get("test_key2")[0].get("count"), 1)

    def test_i_yes_already_answered(self):
        """Check if the poll already is answered, should be False."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "aa",
                                        "n": "1",
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"y")

    def test_j_view_nonexist_poll(self):
        """Check if navigating to non existant poll will provide a way for user to go back."""
        response = self.client.get("/poll/80085")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Go back to polls" in str(response.content, encoding="UTF-8"))

    def test_k_result_nonexist_poll(self):
        """Check if navigating to non existant poll's results will.

        provide a way for user to go back.
        """
        response = self.client.get("/res/80085")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Go back to polls" in str(response.content, encoding="UTF-8"))

    def test_l_result_view_poll_no_perm(self):
        """Check if viewing poll results without permission work."""
        response = self.client.get("/res/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("not have permission to view" in str(response.content,
                                                             encoding="UTF-8"))

    def test_m_result_view_poll_yes_perm(self):
        """Check if viewing poll results work."""
        self.client.cookies = self.__class__.cookies
        response = self.client.get("/res/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("test_key2" in str(response.content, encoding="UTF-8"))
        self.assertTrue("test_val2" in str(response.content, encoding="UTF-8"))

    def test_n_poll_view_yes_perm(self):
        """Check if viewing poll results work."""
        self.client.cookies = self.__class__.cookies
        response = self.client.get("/poll/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "yml_data here" in str(response.content, encoding="UTF-8"))

    def test_n_poll_view_no_perm(self):
        """Check if viewing poll results without perm work."""
        response = self.client.get("/poll/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "yml_data here" not in str(response.content, encoding="UTF-8"))

    def test_o_creator_login_redirect(self):
        """Check if visitor will get redirected in creator."""
        response = self.client.get("/create/")
        self.assertEqual(response.status_code, 302)

    def test_p_creator_view(self):
        """Check creator view shows if authenticated."""
        self.client.cookies = self.__class__.cookies
        response = self.client.get("/create/")
        self.assertEqual(response.status_code, 200)

    def test_q_creator_view_edit_nonexist(self):
        """Check if you can edit non existing poll."""
        self.client.cookies = self.__class__.cookies
        response = self.client.get("/create/80085")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Failed to load poll" in str(response.content, encoding="UTF-8"))

    def test_r_creator_view_edit(self):
        """Check if you can edit an existing poll."""
        self.client.cookies = self.__class__.cookies
        response = self.client.get("/create/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("vue" in str(b''.join(response.streaming_content),
                                     encoding="UTF-8"))

    def test_s_creator_view_polls_view(self):
        """Check if you can edit an existing poll."""
        response = self.client.get("/polls")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("New Poll" in str(response.content, encoding="UTF-8"))

    def test_t_api_get_nonexist(self):
        """Check if you can get an non existing poll."""
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "get",
                                        "n": "80085"
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_u_submit_nonexist(self):
        """Submit the poll response for a non existing poll."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "submit",
                                        "n": "80085",
                                        "r": {
                                            "test_key": "test_val"
                                        }
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_v_submit_no_auth(self):
        """Submit the poll response without auth for auth-required poll."""
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "submit",
                                        "n": "1",
                                        "r": {
                                            "test_key": "test_val"
                                        }
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_w_create_type_check(self):
        """Create a poll with bad types."""
        self.client.cookies = self.__class__.cookies
        orig = {
            "f": "create",
            "n": "New Poll",
            "i": "https://localhost:80/logo.png",
            "a": 2,
            "r": 2,
            "b": 0,
            "y": "yml_data here"
        }
        cur = dict(orig)
        cur["y"] = 80085
        response = self.client.post("/gyatt",
                                    data=dumps(cur),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        cur = dict(orig)
        cur["n"] = 80085
        response = self.client.post("/gyatt",
                                    data=dumps(cur),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        cur = dict(orig)
        cur["r"] = "gay"
        response = self.client.post("/gyatt",
                                    data=dumps(cur),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        cur = dict(orig)
        cur["i"] = 80085
        response = self.client.post("/gyatt",
                                    data=dumps(cur),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        cur = dict(orig)
        cur["a"] = "ass"
        response = self.client.post("/gyatt",
                                    data=dumps(cur),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        cur = dict(orig)
        cur["c"] = "shit"
        response = self.client.post("/gyatt",
                                    data=dumps(cur),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        cur = dict(orig)
        cur["c"] = 0xFFFFFFFF
        cur["a"] = 0
        cur["r"] = 0
        response = self.client.post("/gyatt",
                                    data=dumps(cur),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        cur = dict(orig)
        cur["b"] = None
        cur["a"] = 1
        cur["r"] = 1
        response = self.client.post("/gyatt",
                                    data=dumps(cur),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        cur = dict(orig)
        cur["a"] = 262144
        response = self.client.post("/gyatt",
                                    data=dumps(cur),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        cur = dict(orig)
        cur["b"] = "AHHH"
        response = self.client.post("/gyatt",
                                    data=dumps(cur),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_x_res_api(self):
        """View poll result."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "res",
                                        "n": "1"
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_y_res_api_bad_poll_number(self):
        """View poll result with bad types."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "res",
                                        "n": 80085
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_za_invalid_rizz(self):
        """Attempt to gyatt a fanum taxed rizz."""
        response = self.client.post("/gyatt",
                                    data=dumps({"f": "DoesNotExist"}),
                                    content_type='application/json')
        self.assertEqual(response.content, b"Function not found")
        self.assertEqual(response.status_code, 404)

    def test_zb_res_api_bad_poll_number(self):
        """View poll result doesn't exist."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "res",
                                        "n": "80085"
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_zc_res_api_no_perm(self):
        """View poll result doesn't exist."""
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "res",
                                        "n": "1"
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_zd_submit_no_need_auth(self):
        """Submit a response for poll that doesn't require auth."""
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "submit",
                                        "n": "2",
                                        "r": {
                                            "test_key": "test_val"
                                        }
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_ze_number_function(self):
        """Attempt to call a number."""
        response = self.client.post("/gyatt",
                                    data=dumps({"f": 80085}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_zf_login_failed(self):
        """Login with invalid credentials."""
        response = self.client.post("/accounts/login/",
                                    data={
                                        "username": "user",
                                        "password": "root"
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Please enter a correct username and password" in str(
            response.content, encoding="UTF-8"))

    def test_zg_basic_view_get_null(self):
        """Test get using empty request on basic view."""
        res = BasicView().get(HttpRequest())
        self.assertEqual(res.status_code, 404)
        req = HttpRequest()
        req.resolver_match = type('Resolver', (object, ),
                                  {'url_name': "DoesNotExist"})()
        res = BasicView().get(req)
        self.assertEqual(res.status_code, 404)

    def test_zh_already_exist_api_non_exist(self):
        """Test the already exist api for non existing poll."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "aa",
                                        "n": "80085",
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_zi_already_exist_api_non_auth(self):
        """Test the already exist api for non authenticated user."""
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "aa",
                                        "n": "1",
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_zj_edit_poll(self):
        """Test editing the poll."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "create",
                                        "n": "New Poll",
                                        "i": "https://localhost:80/logo.png",
                                        "a": 2,
                                        "r": 2,
                                        "b": 0,
                                        "e": 1,
                                        "y": "toml_data here"
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'1')

    def test_zk_edit_non_exist_poll(self):
        """Test editing the poll."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "create",
                                        "n": "New Poll",
                                        "i": "https://localhost:80/logo.png",
                                        "a": 2,
                                        "r": 2,
                                        "b": 0,
                                        "e": 80085,
                                        "y": "toml_data here"
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_zl_view_any_res(self):
        """View poll result as guest for poll whoose result can be view by anyone."""
        response = self.client.get("/poll/2")
        self.assertEqual(response.status_code, 200)

    def test_zm_view_res_creator(self):
        """View poll result as creator."""
        self.client.cookies = self.__class__.cookies
        response = self.client.get("/poll/3")
        self.assertEqual(response.status_code, 200)

    def test_zn_login(self):
        """Login as other account."""
        response = self.client.post("/accounts/login/",
                                    data={
                                        "username": "user2",
                                        "password": "1234"
                                    })
        self.__class__.cookies = response.cookies
        self.assertEqual(response.status_code, 302)

    def test_zo_edit_not_mine_poll(self):
        """Test editing the poll."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "create",
                                        "n": "New Poll",
                                        "i": "https://localhost:80/logo.png",
                                        "a": 2,
                                        "r": 2,
                                        "b": 0,
                                        "e": 1,
                                        "y": "toml_data here"
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_zp_view_poll_other(self):
        """Test viewing a CLIENT poll."""
        self.client.cookies = self.__class__.cookies
        response = self.client.get("/poll/4")
        self.assertEqual(response.status_code, 200)

    def test_zq_submit_same_key(self):
        """Test viewing a CLIENT poll."""
        self.client.cookies = self.__class__.cookies
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "submit",
                                        "n": "1",
                                        "r": {
                                            "test_key2": "WAIT_TEST"
                                        }
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_zr_res_same_key(self):
        """Test viewing a CLIENT poll."""
        self.client.cookies = self.__class__.cookies
        response = self.client.get("/res/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'WAIT_TEST' in response.content)

    def test_zz_logout(self):
        """Logout."""
        self.cookies = self.__class__.cookies
        response = self.client.post("/accounts/logout/",
                                    HTTP_X_FORWARDED_FOR="8.8.8.8")
        self.assertEqual(response.status_code, 302)
