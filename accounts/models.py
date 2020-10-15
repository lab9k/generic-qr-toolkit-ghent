from django.db import models
from django.contrib.auth.models import AbstractUser
from api.models import Department


class User(AbstractUser):
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
