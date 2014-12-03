from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Greeting(models.Model):
    author = models.ForeignKey(User, null=True, blank=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)