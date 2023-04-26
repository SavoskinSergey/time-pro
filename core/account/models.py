from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from core.abstract.models import AbstractModel, AbstractManager
from phonenumber_field.modelfields import PhoneNumberField


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.public_id}/{filename}'


class UserManager(BaseUserManager, AbstractManager):

    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a `User` with an email, phone number,
            username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')
        if password is None:
            raise TypeError('User must have an email.')

        user = self.model(
            username=username,
            email=self.normalize_email(email), **kwargs
            )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **kwargs):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(db_index=True, unique=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    avatar = models.ImageField(
                    null=True, blank=True, upload_to=user_directory_path
                    )
    note = models.TextField(null=True, blank=True)

    # events_subscribed = models.ManyToManyField(
    #     'core_event.Event',
    #     related_name='subscribed_by'
    # )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    # def subscribe(self, event):
    #     """Subscribe 'event' if it hasn't been done yet"""
    #     return self.events_subscribed.add(event)

    # def remove_subscribe(self, event):
    #     """Remove a subscribe from a 'event'"""
    #     return self.events_subscribed.remove(event)

    # def has_subscribed(self, event):
    #     """Return True if the user has subscribed a 'event'; else False"""
    #     return self.events_subscribed.filter(pk=event.pk).exists()
