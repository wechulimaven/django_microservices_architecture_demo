from django.db.models import TextChoices


class NotificationChannels(TextChoices):
    sms = "sms"
    email = "email"