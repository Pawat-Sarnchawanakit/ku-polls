from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    password_hash = models.BinaryField(max_length=64)
    password_salt = models.BinaryField(max_length=64)

class Poll(models.Model):
    name = models.CharField(max_length=100, default='Unnamed Poll')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    allow = models.IntegerField(default=0)
    image = models.CharField(max_length=256, default='')
    yaml = models.CharField(max_length=4096*8)
    pub_date = models.DateTimeField(auto_now_add=True)

class Response(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accessed = models.DateTimeField(auto_now_add=True)
    session = models.BinaryField(max_length=64, unique=True, editable=False, primary_key=True)