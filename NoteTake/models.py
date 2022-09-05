from re import U
from django.db import models

class User(models.Model):
    userid = models.CharField(max_length=1000)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=8)


class Note(models.Model):
    userid = models.CharField(max_length=1000)
    date = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=100000)