from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError

from services.post_service import PostService
from services.user_service import UserService


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)

    def create(self, validated_data):
        user_service = UserService()
        __, user = user_service.login_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        print(user)
        return user


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    bio = serializers.CharField(required=False)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, trim_whitespace=False)
    confirm_password = serializers.CharField(required=True,trim_whitespace=False)
    phone_number = serializers.CharField(required=True)

    def create(self, validated_data):
        user_service = UserService()
        __, user = user_service.register_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            bio=validated_data["bio"],
            password=validated_data["password"],
            confirm_password=validated_data["confirm_password"],
        )
        # if not success:
        #     raise DjangoValidationError(user)
        return user


class PostSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    image = serializers.ImageField(required=False)

    def create(self, validate_data):
        post_service = PostService()
        __, feed = post_service.add_feed(
            user_id=validate_data["user_id"],
            title=validate_data["title"],
            body=validate_data["body"],
            image=validate_data.get("image", None),
        )
        # if not success:
        #     raise DjangoValidationError(feed)
        return feed
