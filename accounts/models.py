from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.db import models

from django_extensions.db.models import TimeStampedModel


class CustomUserManager(BaseUserManager):

    def _create_user(self,
                     email,
                     password=None,
                     is_superuser=False
                     ):
        if not email:
            raise ValueError('You must provide an email address.')

        user = self.model(
            email=self.normalize_email(email),
            is_superuser=is_superuser
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None):
        return self._create_user(email, password)

    def create_superuser(self,
                         email,
                         password,
                         is_superuser=True
                         ):
        return self._create_user(
            email,
            password,
            is_superuser
        )


class CustomUser(AbstractBaseUser, TimeStampedModel, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
