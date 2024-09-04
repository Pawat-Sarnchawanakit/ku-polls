"""Contain tests."""
from json import dumps, loads
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
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
        with open("test.html", "wb") as f:
            f.write(response.content)
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

    def test_z_invalid_rizz(self):
        """Attempt to gyatt a fanum taxed rizz."""
        response = self.client.post("/gyatt",
                                    data=dumps({"f": "DoesNotExist"}),
                                    content_type='application/json')
        self.assertEqual(response.content, b"Function not found")
        self.assertEqual(response.status_code, 404)
