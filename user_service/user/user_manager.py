from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import exceptions


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _get_active_api_user_queryset(self):
        return self.filter(is_staff=False, is_active=True)

    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        extra_fields["username"] = email
        user = self.model(email=email, **extra_fields)

        try:
            validate_password(password, user)
        except ValidationError as e:
            raise exceptions.ValidationError({"password": e.messages})
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)