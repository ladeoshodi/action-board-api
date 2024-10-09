from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_img = models.URLField(max_length=200, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
