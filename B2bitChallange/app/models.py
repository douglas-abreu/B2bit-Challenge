from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import re

class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, is_superuser=is_superuser, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)
    def create_superuser(self, email, password, **extra_fields):
        user=self._create_user(email, password, True, True, **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user


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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = BaseUserManager()

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



    REQUIRED_FIELDS = ['usercustom', 'title', 'content']