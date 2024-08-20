from django.db import models

class Poll(models.Model):
    name = models.CharField(max_length=100, default='Unnamed Poll')
    image = models.CharField(max_length=256, default='')
    yaml = models.CharField(max_length=4096*8)
    pub_date = models.DateTimeField(auto_now_add=True)

class Response(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)