from post_service.celery import app as celery_app

from services.user_api_service import UserService
from services.notification_service import NotificationService


@celery_app.task(name="send_post_notification")
def send_post_notification(user_id, message, channel, email=None, phone=None):
    user_ser = UserService()
    all_active_users = user_ser.get_all_users()
    ids = []
    for i in all_active_users:
        ids.append(i["id"])
    service = NotificationService(
        user_ids=ids, channel=channel, email=email, phone=phone
    )
    service.send_notification(message=message)
