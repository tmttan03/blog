import uuid
import hashlib
from time import gmtime, strftime

from datetime import timedelta as delta, datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """ Account User Information. """

    email = models.EmailField(max_length=500, unique=True)
    username = models.CharField(max_length=80, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=80, null=True, blank=True)
    avatar = models.ImageField(upload_to='profile_pics', default='/default/img.jpg')
    header = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name",)

    objects = UserManager()

    def __str__(self):
        return "{}".format(self.email)

    def get_full_name(self):
        """Return User's Complete Name."""

        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name.title(),
                                  self.last_name.title())
        return self.email


class ForgotPassword(models.Model):
    PENDING = 1
    USED = 2

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (USED, 'Used')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, blank=True)
    status = models.IntegerField(default=PENDING, choices=STATUS_CHOICES)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.user, self.status)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            # Set token
            curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            string_to_hash = "{}{}".format(self.user.email, curr_time)
            self.token = hashlib.sha256(string_to_hash.encode('utf-8')).hexdigest()

            try:
                confirm_link = settings.WEBAPP_RESET_PASSWORD_PATH
            except Exception as e:
                raise ValueError("Missing setting: WEBAPP_RESET_PASSWORD_URL")

            base_url = "{}{}/".format(settings.PROTOCOL, settings.DOMAIN_NAME)
            token_link = "{}{}/?token={}".format(base_url, confirm_link, self.token)

            email_context = {
                'token': token_link,
                'full_name': self.user.get_full_name()
            }

            # Email templates
            email_plain = render_to_string('email/reset_password/email.txt', email_context)
            email_html = render_to_string('email/reset_password/email.html', email_context)

            # Send email to user
            send_mail(
                'Blog - Reset Password',
                email_plain,
                settings.DEFAULT_FROM_EMAIL,
                [self.user.email],
                html_message=email_html,
            )
        super(ForgotPassword, self).save()


class Follower(models.Model):
    ACTIVE = 1
    INACTIVE = 2

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_user')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_followed')
    status = models.IntegerField(default=ACTIVE, choices=STATUS_CHOICES)
    date_followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} followed {}".format(self.user, self.followed)