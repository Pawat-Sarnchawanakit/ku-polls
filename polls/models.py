from django.db import models
from django.utils import timezone


class User(models.Model):
    """Contains User data like password hash, salt, username, and account creation date.
    """
    username = models.CharField(max_length=50,
                                unique=True,
                                editable=False,
                                primary_key=True)
    # Creation date.
    created = models.DateTimeField(default=timezone.now)
    password_hash = models.BinaryField(max_length=64)
    password_salt = models.BinaryField(max_length=64)



class Poll(models.Model):
    """The polls which will be listed in the home page.
    """
    name = models.CharField(max_length=100, default='Unnamed Poll')
    # Id of who created the poll.
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    # Who is allowed to submit responses to the poll, authenticated users only? etc...
    allow = models.IntegerField(default=0)
    # Who is allowed to view the result of the poll.
    res = models.IntegerField(default=0)
    # The thumbnail image of the poll.
    image = models.CharField(max_length=256, default='')
    # The actual poll data in yaml.
    yaml = models.CharField(max_length=4096 * 8)
    # The date the poll is published.
    pub_date = models.DateTimeField()



class Response(models.Model):
    """Reponse of the polls.
    """
    # What poll does this response belong to?
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    # Who wrote this response? NULL if the one who responded is not authenticated.
    submitter = models.ForeignKey(User,
                                  default=None,
                                  null=True,
                                  on_delete=models.CASCADE)
    # What `question` does this response answer?
    key = models.CharField(max_length=200)
    # What is the answer to that question?
    value = models.CharField(max_length=200)




class Session(models.Model):
    """Used to keep users logged in.
    """
    # The user the session belongs to.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The time this session was last accessed.
    accessed = models.DateTimeField(auto_now_add=True)
    # The session id, will be kept as a COOKIE on the user's browser.
    session = models.BinaryField(max_length=64,
                                 unique=True,
                                 editable=False,
                                 primary_key=True)
