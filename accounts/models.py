from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

# Create your models here.




class CustomAccountManager(BaseUserManager):

    def create_superuser(self, mobile_number, password=None, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(mobile_number, password, **other_fields)

    def create_user(self, mobile_number, password=None, **other_fields):

        if not mobile_number:
            raise ValueError(_('You must provide an mobile number !'))

        user = self.model(mobile_number=mobile_number, **other_fields)

        if password is not None:
            user.set_password(mobile_number)

        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    STATUS_CHOICES = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('banned', 'banned'),
    )

    # user_type => patient | doctor | hospital | admin
    user_type = models.CharField(max_length=16, default="patient")
    mobile_number = models.CharField(max_length=16, unique=True)

    full_name = models.CharField(max_length=64, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(max_length=512, blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=16, blank=True, null=True, choices=STATUS_CHOICES)  # active, inactive, banned

    is_staff = models.BooleanField(default=False)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    objects = CustomAccountManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.mobile_number




