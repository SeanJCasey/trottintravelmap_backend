from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.db import models

from django_extensions.db.models import TimeStampedModel
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):

    def _create_user(self,
                     email,
                     name,
                     password=None,
                     is_superuser=False
                     ):
        if not email:
            raise ValueError('You must provide an email address.')

        if not name:
            raise ValueError('You must provide a name.')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            is_superuser=is_superuser
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password=None):
        return self._create_user(email, name, password)

    def create_superuser(self,
                         email,
                         name,
                         password,
                         is_superuser=True
                         ):
        return self._create_user(
            email,
            name,
            password,
            is_superuser
        )


class CustomUser(AbstractBaseUser, TimeStampedModel, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=70, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def _generate_unique_slug(self):
        slug = orig = slugify(self.name)
        counter = 1
        while CustomUser.objects.filter(slug=slug).exists():
            slug = '{}-{}'.format(orig, counter)
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        print(self.slug)
        print(slugify(self.name))
        if not self.slug:
            self.slug = self._generate_unique_slug()

        super().save(*args, **kwargs)
