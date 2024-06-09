from django.urls import path
from .views import SendNotification

urlpatterns = [
    path('send-notification/', SendNotification.as_view(), name='send_notification'),
]
