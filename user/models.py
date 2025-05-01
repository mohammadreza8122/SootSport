from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUserManager(UserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('ایمیل الزامی است')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):

    gender_types = [("Male", "Male"), ("Female", "Female")]
    gender = models.CharField(max_length=10,
                              blank=True,
                              null=True,
                              choices=gender_types)
    job_types = [
        ("Admin", "Admin"),
        ("User", "User"),
        ("Support", "Support"),
        ("Coach", "Coach"),
        ("Store", "Store"),
        ("Provider", "Provider"),
    ]
    job = models.CharField(max_length=10, choices=job_types, default="User")

    phone_number = models.CharField(max_length=30, null=True, blank=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)
    reject_comment = models.TextField(null=True, blank=True)

    email = models.EmailField(_('email address'), null=True, blank=True)

    # NullBooleanField is deprecated, use BooleanField with null=True instead
    is_user_active = models.BooleanField(null=True, default=False)
    is_complete_data = models.BooleanField(null=True, default=False)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = self.phone_number
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date_joined"]


class ProfilePic(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    profile_pic = models.ImageField(upload_to="photos/profile/")

    def __str__(self):
        return "image for user %s" % (self.user)


class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return self.expires_at > timezone.now()