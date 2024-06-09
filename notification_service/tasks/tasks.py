from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@shared_task
def send_notification(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{user_id}",
        {
            'type': 'send_notification',
            'message': message,
        }
    )
