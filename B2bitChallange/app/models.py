from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import datetime
import re


class User(AbstractBaseUser, PermissionsMixin):
    """User model

    Used to keep all users from the system.
    """

    email = models.EmailField(
        unique=True)
    first_name = models.CharField(
        max_length=30)
    last_name = models.CharField(
        max_length=30)
    is_staff = models.BooleanField(
        default=False)
    is_active = models.BooleanField(
        default=True)
    date_joined = models.DateTimeField(
        default=datetime.datetime.now,
        editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class Publication(models.Model):
    """Publication model

    Used to keep all publications made by users.
    """

    usercustom = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True)
    title = models.CharField(
        max_length=100)
    content = models.CharField(
        max_length=250)

    REQUIRED_FIELDS = ['title', 'content']