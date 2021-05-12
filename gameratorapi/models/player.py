from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    catch_phrase = models.CharField(max_length=100)