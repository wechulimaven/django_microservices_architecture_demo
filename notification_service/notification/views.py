import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from notification.services.email_service import SendEmailService
from notification.services.sms_service import SMSClient
from .serializers import NotificationSerializer
from django.shortcuts import render

logger = logging.getLogger(__name__)


class SendNotification(APIView):
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            user_ids = serializer.validated_data['user_ids']
            message = serializer.validated_data['message']
            channel = serializer.validated_data['channel']
            phone = serializer.validated_data['phone']
            email = serializer.validated_data['email']
            channel_layer = get_channel_layer()
            for user_id in user_ids:
                logger.info(f"******{user_id}*****")
                group_name = f"user_{user_id}"

                async_to_sync(channel_layer.group_send)(
                    group_name,
                    {
                        'type': 'send_notification',
                        'message': message
                    }
                )

                if(channel=="email" and email is not None):
                    email_service=SendEmailService(email=email)
                    email_service.send(message=message)

                if(channel=="sms" and phone is not None):
                    sms_service=SMSClient(recepient=phone, message=message)
                    sms_service.send()

                return Response({"status":True, "message":"Notification send", "data":{}}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def notification_page(request):
    return render(request, 'notification/notification.html')
