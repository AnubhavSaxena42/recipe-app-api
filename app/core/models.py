"""
Database models
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager


class UserManager(BaseUserManager):
    """Manager for our custom user model"""

    def create_user(self,email,password=None,**extra_fields):
        """Create,Save and return a new user"""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
                email=self.normalize_email(email),
                **extra_fields,
            )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password=None,**extra_fields):
        """Creates a superuser in the database"""

        user = self.create_user(email,password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    """Custom User model for the project"""

    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()