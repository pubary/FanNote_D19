from django.contrib.auth.models import AbstractUser
from django.db import models


class FunUser(AbstractUser):
    code = models.CharField(max_length=63, blank=True)
