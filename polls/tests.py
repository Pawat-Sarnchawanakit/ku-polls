from django.test import TestCase
from json import dumps, loads

# to store session cookie
session = None


class APITest(TestCase):
    # Bro quit rolling back my test database.
    @classmethod
    def _rollback_atomics(cls, atomics):
        return

    def test_a_list_empty(self):
        """List empty, no polls are added yet.
        """
        response = self.client.post("/gyatt",
                                    data=dumps({"f": "list"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'[]')

    def test_b_create_account(self):
        """Create an account.
        """
        global session
        response = self.client.post("/gyatt",
                                    data=dumps({
                                        "f": "regis",
                                        "u": "User",
                                        "p": "1234"
                                    }),
                                    content_type='application/json')
        self.assertTrue(response.cookies["tk"] is not None,
                        "`tk` cookie should be set.")
        session = response.cookies
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'ok')

    def test_c_create_poll(self):
        """Create a poll.
        """
        self.client.cookies = session
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

    def test_d_list_one(self):
        """List one poll.
        """
        response = self.client.post("/gyatt",
                                    data=dumps({"f": "list"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "New Poll")
        self.assertEqual(data[0]["image"], "https://localhost:80/logo.png")

    def test_e_invalid_rizz(self):
        """Attempt to gyatt a fanum taxed rizz.
        """
        response = self.client.post("/gyatt",
                                    data=dumps({"f": "DoesNotExist"}),
                                    content_type='application/json')
        self.assertEqual(response.content, b"bad")
        self.assertEqual(response.status_code, 400)
