from django.db import models
from django.conf import settings

# Create your models here.

class Book(models.Model):
    book_id = models.CharField(max_length=256)
    book_name = models.CharField(max_length=256)
    user_creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='book_user_creator', null=True)
    is_demo = models.BooleanField()

class Dummy(models.Model): pass


