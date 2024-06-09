from rest_framework import serializers

class NotificationSerializer(serializers.Serializer):
    user_ids = serializers.ListSerializer(child=serializers.CharField())
    message = serializers.CharField(max_length=255)
    channel = serializers.CharField(max_length=10)
    email=serializers.EmailField(allow_blank=True)
    phone=serializers.CharField(max_length=12, allow_blank=True)
