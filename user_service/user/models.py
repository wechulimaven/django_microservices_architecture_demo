from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError

from user.user_manager import UserManager
from utils.choices import NotificationChannels

# Create your models here.


def validate_min_length(value):
    if value and len(value) < 2:
        raise ValidationError(
            "Enter valid length of characters.", params={"value": value}
        )

class User(AbstractUser):
    id = models.CharField(
        primary_key=True,
        default=uuid.uuid4().hex,
        editable=False,
        db_index=True,
        max_length=128,
    )

    first_name = models.CharField(
        "first name", max_length=150, validators=[validate_min_length]
    )
    last_name = models.CharField(
        "last name", max_length=150, validators=[validate_min_length]
    )
    email = models.EmailField("email address", unique=True)
    avatar = models.ImageField(
        upload_to="avatars/", max_length=254, blank=True, null=True
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.CharField(max_length=1500, blank=True, null=True)
    notification_channel = models.CharField(max_length=1500, blank=True, null=True, choices=NotificationChannels.choices, default=NotificationChannels.email)

    objects = UserManager()


    def __str__(self):
        return f"{self.username} {self.account_type}"




