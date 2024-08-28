"""Contains models."""
import enum
import hmac
import secrets
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.db.models import Count


def get_or_none(model_class, **kwargs):
    """Get a model, returns None if not found.

    Args:
        model_class (class): The model class to get.

    Returns:
        model_class | None: The obtained model class or None
    """
    try:
        return model_class.objects.get(**kwargs)
    except model_class.DoesNotExist:
        return None


class BitEnum(enum.Enum):
    """An enum that acts like an array of booleans."""

    def has(self, val: int) -> bool:
        """Check whether an enum is active.

        Args:
            val (int): The value to check.

        Returns:
            bool: Whether the enum is active.
        """
        return (val & self.value) != 0


class AuthType(BitEnum):
    """The authentication type for polls.

    To allow certain groups of people to vote.
    """

    CLIENT = 1
    AUTH = 1 << 1


class ResType(BitEnum):
    """Poll viewing permission.

    The Enum that specified who has
    permission to view the results of a poll.
    """

    CREATOR = 1
    AUTH = 1 << 1


class User(models.Model):
    """Contain User data.

    Such as password hash, salt,
    username, and account creation date.
    """

    username = models.CharField(max_length=50,
                                unique=True,
                                editable=False,
                                primary_key=True)
    # Creation date.
    created = models.DateTimeField(default=timezone.now)
    password_hash = models.BinaryField(max_length=64)
    password_salt = models.BinaryField(max_length=64)

    def check_password(self, password: str) -> bool:
        """Check whether the given password is correct for this user.

        Args:
            password (str): The password to check.

        Returns:
            bool: Whether the password is correct
        """
        return hmac.compare_digest(
            hmac.digest(self.password_salt, bytes(password, "utf-8"),
                        "blake2b"), self.password_hash)

    def create_session(self) -> str:
        """Create a session for a user.

        Returns:
            string: The session key created.
        """
        # Remove sessions older than 30 days.
        Session.objects.filter(user=self,
                               accessed__lte=timezone.now() -
                               timedelta(days=30)).delete()
        # Create session
        session_key = secrets.token_bytes(64)
        session = Session(user=self, session=session_key)
        session.save()
        return session_key

    @classmethod
    def register(cls, username: str, password: str):
        """Register a user.

        Args:
            username (str): The user's name.
            password (str): The user's password.
        """
        salt = secrets.token_bytes(64)
        pw_hash = hmac.digest(salt, bytes(password, "UTF-8"), "blake2b")
        return cls.objects.create(username=username,
                                  password_hash=pw_hash,
                                  password_salt=salt)


class Poll(models.Model):
    """The polls which will be listed in the home page."""

    name = models.CharField(max_length=100, default='Unnamed Poll')
    # Id of who created the poll.
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    # Who is allowed to submit responses to the poll,
    # authenticated users only? etc...
    allow = models.IntegerField(default=0)
    # Who is allowed to view the result of the poll.
    res = models.IntegerField(default=0)
    # The thumbnail image of the poll.
    image = models.CharField(max_length=256, default='')
    # The actual poll data in yaml.
    yaml = models.CharField(max_length=4096 * 8)
    # The date the poll is published.
    pub_date = models.DateTimeField(default=timezone.now)
    # The date the poll won't accept a  ny more answers.
    end_date = models.DateTimeField(null=True, default=None)

    def get_responses(self) -> dict:
        """Get the responses.

        Returns:
            The response dict, with value and count.
        """
        responses_list = Response.objects.filter(question=self) \
            .values("key", "value") \
            .annotate(count=Count("value"))
        responses_dict = dict()
        for v in responses_list:
            val = responses_dict.get(v["key"])
            if val is None:
                val = []
                responses_dict[v["key"]] = val
            val.append({"value": v["value"], "count": v["count"]})
        return responses_dict

    def is_published(self) -> bool:
        """Check whether the poll is accepting responses.

        Returns:
            bool: True if the poll is accepting responses otherwise False.
        """
        return self.pub_date <= timezone.now()

    def is_closed(self) -> bool:
        """Check whether the poll has already been closed.

        Returns:
            bool: True if the poll is already closed.
        """
        return self.end_date is not None and timezone.now() >= self.end_date

    def is_visible(self) -> bool:
        """Return true if the poll should be listed.

        Returns:
            True if the poll should be listed.
        """
        return self.is_published() and not self.is_closed()

    def can_vote(self, user: User | None) -> bool:
        """Check if a user can vote.

        Check whether a particular user, or an annoynamous user
        has the permission to vote in a poll.

        Args:
            user (User | None): The user, or None if annoynamous.

        Returns:
            bool: Whether they can vote.
        """
        if not self.is_visible():
            return False
        # 0 means allow anyone to vote.
        if self.allow == 0:
            return True
        # If authenticated, check that.
        if AuthType.AUTH.has(self.allow):
            # If authenticated, prefer db check over client check.
            if user is None:
                return False
            return True
        # Check is done on the client,
        # if we received a request it means they can vote.
        if AuthType.CLIENT.has(self.allow):
            return True
        return False

    def can_view(self, user: User | None):
        """Check whether a user can view a poll.

        Args:
            user (User | None): The user or None if annoynomous.

        Returns:
            bool: Whether such person can view the poll.
        """
        return (user is not None
                and user == self.creator) or self.can_vote(user)

    def requires_auth(self):
        """Check whether the poll requires authentication to submit.

        Returns:
            bool: Whether the poll requires authentication.
        """
        return (self.allow != 0 and not AuthType.CLIENT.has(self.allow)
                and AuthType.AUTH.has(self.allow))

    def can_view_responses(self, user: User | None):
        """Check if a user can view responses.

        Check whether a particular user, or an annoynamous user
        has the permission to view responses of a poll.

        Args:
            user (User | None): The user, or None if annoynamous.

        Returns:
            bool: Whether they can view responses.
        """
        if self.res == 0:
            # Anyone can view responses.
            return True
        if user is not None and ResType.AUTH.has(self.res):
            # Any authenticated users can view responses.
            return True
        if user is not None and ResType.CREATOR.has(
                self.res) and self.creator == user:
            # Creator can view responses.
            return True
        return False


class Response(models.Model):
    """Reponse of the polls."""

    # What poll does this response belong to?
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    # Who wrote this response?
    # NULL if the one who responded is not authenticated.
    submitter = models.ForeignKey(User,
                                  default=None,
                                  null=True,
                                  on_delete=models.CASCADE)
    # What `question` does this response answer?
    key = models.CharField(max_length=200)
    # What is the answer to that question?
    value = models.CharField(max_length=200)


class Session(models.Model):
    """Used to keep users logged in."""

    # The user the session belongs to.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The time this session was last accessed.
    accessed = models.DateTimeField(auto_now_add=True)
    # The session id, will be kept as a COOKIE on the user's browser.
    session = models.BinaryField(max_length=64,
                                 unique=True,
                                 editable=False,
                                 primary_key=True)
