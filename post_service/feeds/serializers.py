from rest_framework import serializers


from django.core.exceptions import ValidationError as DjangoValidationError

from task.tasks import send_post_notification
from services.user_api_service import UserService

from .models import Post


class PostBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            "id",
            "user_id",
            "title",
            "body",
            "image",
        )
        read_only_fields = (
            "id", 
        )

    def validate(self, data):
        userId = data["user_id"]
        userService = UserService()
        success, user = userService.get_user_detail(userId)
        if not success:
            raise DjangoValidationError(user)
        data["user"] = user
        return data

    def create(self, validated_data):
        try:
            print(validated_data)
            user_obj = validated_data.pop("user")
            post = super().create(validated_data)
            if(user_obj["is_active"]):
                message = f"A {validated_data['title']} post is available for you. "
                send_post_notification.delay(
                    user_id=user_obj["id"],
                    message=message,
                    channel=user_obj["notification_channel"],
                    email=user_obj["email"],
                    phone=user_obj["phone_number"],
                )

            return post
        except Exception as e:
            raise DjangoValidationError(e)


class PostDetailSerializer(PostBaseSerializer):

    user = serializers.SerializerMethodField()

    class Meta(PostBaseSerializer.Meta):
        fields = PostBaseSerializer.Meta.fields + ("user",)

    def get_user(self, obj):
        userService = UserService()
        success, user = userService.get_user_detail(user_id=obj.user_id)
        if success:
            return user
