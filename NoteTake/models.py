from django.db import models

class User(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=8)


class Note(models.Model):
    date = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=100000)