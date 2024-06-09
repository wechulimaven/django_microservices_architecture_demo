from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

import os

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError


from .models import User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(trim_whitespace=False, write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if password and username:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if user.is_staff:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        data["user"] = user
        return data

    def create(self, validated_data):
        user = validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        user.last_login = timezone.now()
        user.save()
        return token, user

    def delete(self):
        user = self.context["request"].user
        Token.objects.filter(user=user).delete()


class UserBaseSerializer(serializers.ModelSerializer):
    interest = serializers.SerializerMethodField()
    goal = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "bio",
            "notification_channel",
            "is_active",
        )
        read_only_fields = (
            "id", 
        )


class UserAccountSerializer(UserBaseSerializer):
    confirm_password = serializers.CharField(
        write_only=True, required=True, allow_blank=False, allow_null=False
    )

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + (
            "email",
            "password",
            "confirm_password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        try:
            django_validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate_email(self, value):
        user_qs = User.objects.filter(email__iexact=value)
        if user_qs.exists():
            raise serializers.ValidationError(
                "user with this email address already exists."
            )
        else:
            return value

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": _("Passwords do not match.")}
            )
        data.pop("confirm_password")
        return data

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            token = Token.objects.get_or_create(user=user)
        return token, user


class UserAccountUpdateSerializer(UserBaseSerializer):
    bio = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    avatar = serializers.ImageField(required=False)
    phone_number = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    class Meta(UserBaseSerializer.Meta):
        pass

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.save()
        return instance
