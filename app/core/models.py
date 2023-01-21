"""
Database models.
"""
from datetime import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Order(models.Model):
    """Order objects."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    start_date_time = models.DateTimeField()
    close_date_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    symbol = models.CharField(max_length=10)
    amount = models.FloatField(null=True)
    stop_loss = models.FloatField()
    take_profit = models.FloatField()
    leverage = models.IntegerField()
    initial_price = models.FloatField()
    closing_price = models.FloatField(
        null=True,
        blank=True,
        )
    title = models.CharField(
        max_length=255,
        default=f'{symbol} order created on {str(start_date_time)}',
        )

    def __str__(self):
        return self.title


class Crypto(models.Model):
    """Crypto historical data objects."""
    date_and_time = models.DateTimeField()
    low = models.FloatField()
    high = models.FloatField()
    open = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    symbol = models.CharField(max_length=10)

    class Meta:
        ordering = ('date_and_time',)

