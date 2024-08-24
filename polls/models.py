from django.db import models
"""Contains User data like password hash, salt, username, and account creation date.
"""


class User(models.Model):
    username = models.CharField(max_length=50,
                                unique=True,
                                editable=False,
                                primary_key=True)
    # Creation date.
    created = models.DateTimeField(auto_now_add=True)
    password_hash = models.BinaryField(max_length=64)
    password_salt = models.BinaryField(max_length=64)


"""The polls which will be listed in the home page.
"""


class Poll(models.Model):
    name = models.CharField(max_length=100, default='Unnamed Poll')
    # Id of who created the poll.
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    # Who is allowed to submit responses to the poll, authenticated users only? etc...
    allow = models.IntegerField(default=0)
    # The thumbnail image of the poll.
    image = models.CharField(max_length=256, default='')
    # The actual poll data in yaml.
    yaml = models.CharField(max_length=4096 * 8)
    # The date the poll is published.
    pub_date = models.DateTimeField(auto_now_add=True)


"""Reponse of the polls.
"""


class Response(models.Model):
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


"""Used to keep users logged in.
"""


class Session(models.Model):
    # The user the session belongs to.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The time this session was last accessed.
    accessed = models.DateTimeField(auto_now_add=True)
    # The session id, will be kept as a COOKIE on the user's browser.
    session = models.BinaryField(max_length=64,
                                 unique=True,
                                 editable=False,
                                 primary_key=True)
