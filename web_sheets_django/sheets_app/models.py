from django.db import models
from django.conf import settings

# Create your models here.

class Sheet(models.Model):
    sheet_id = models.CharField(max_length=256)
    sheet_name = models.CharField(max_length=256)
    user_creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sheet_user_creator')

class Dummy(models.Model): pass


