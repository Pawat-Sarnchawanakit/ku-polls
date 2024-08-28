"""Contain tests."""
from json import dumps, loads
from django.test import TestCase
from polls.models import User


class APITest(TestCase):
    """Implement tests for gyatt."""

    # to store session cookie
    session = None

    @classmethod
    def _rollback_atomics(cls, atomics):
        """Override the rollback function.

        To stop the rollback of the database for every test.
        """
        return

    def test_a_list_empty(self):
        """Get the list of polls.

        The list should be empty, no polls are added yet.
        """
        response = self.client.post("/gyatt",
                                    data=dumps({"f": "list"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'[]')

    def test_b_create_account(self):
        """Create an account."""
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "regis",
                                        "u": "User",
                                        "p": "1234"
                                    }),
                                    content_type='application/json')
        self.assertIsNotNone(response.cookies.get("tk"),
                             "`tk` cookie should be set.")
        self.assertIsNotNone(
            User.objects.filter(username="User").first,
            "User should be created.")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'ok')
        self.__class__.session = response.cookies

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
        self.client.cookies = self.__class__.session
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

    def test_e_get_poll(self):
        """Get a poll."""
        self.client.cookies = self.__class__.session
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
        self.client.cookies = self.__class__.session
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "aa",
                                        "n": "1",
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"n")

    def test_g_list_one(self):
        """List one poll."""
        response = self.client.post("/gyatt",
                                    data=dumps({"f": "list"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "New Poll")
        self.assertEqual(data[0]["image"], "https://localhost:80/logo.png")

    def test_f_submit(self):
        """Submit the poll response."""
        self.client.cookies = self.__class__.session
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
        self.client.cookies = self.__class__.session
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
        """Submit the poll response."""
        self.client.cookies = self.__class__.session
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "res",
                                        "n": "1"
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = loads(response.content)
        self.assertIsNone(data.get("test_key"))
        self.assertIsNotNone(data.get("test_key2"))
        self.assertEqual(data.get("test_key2")[0].get("value"), "test_val2")
        self.assertEqual(data.get("test_key2")[0].get("count"), 1)

    def test_i_yes_already_answered(self):
        """Check if the poll already is answered, should be False."""
        self.client.cookies = self.__class__.session
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
