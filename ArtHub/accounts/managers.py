from django.contrib.auth import base_user as auth_base, get_user_model
from django.contrib.auth.hashers import make_password
from django.db import models

# from ArtHub.accounts.models import ArtHubUser

# UserModel = get_user_model()


class ArtHubManager(auth_base.BaseUserManager):

    def _create_user(self, username, password, type, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, type=type, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, type, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # extra_fields.setdefault('type', 'REGULAR_USER')
        return self._create_user(username, password, type, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


