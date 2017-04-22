from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Token(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=200, default="")


# personal info for the user.
class Info(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=40, unique=True, editable=False)
    email = models.EmailField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField(default="", blank=True)
    short_bio = models.CharField(max_length=200, default="", blank=True)
    # want the image to be default one.
    profile_img = models.ImageField(upload_to="profile_image/", blank=True, default="profile_image/default.png")

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name