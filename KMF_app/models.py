from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    business_type = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    groups = models.ManyToManyField('auth.Group', related_name='customuser_groups', blank=True, null=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_user_permissions', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        permissions = [
            ("can_change_settings", "Can change settings"),
        ]

    objects = UserManager()