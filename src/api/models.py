from django.db import models

class Poll(models.Model):
    yaml = models.CharField(max_length=4096*8)
    pub_date = models.DateTimeField(auto_now_add=True)

class Input(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)

class Choice(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)