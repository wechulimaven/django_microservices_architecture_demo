from django.contrib import admin
from django.urls import path, include
from notification.views import notification_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notifications/', notification_page, name='notifications'),
    path('api/v1/', include('notification.urls')),
]
