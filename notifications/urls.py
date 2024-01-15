from django.urls import path
from .views import get_notifications, mark_notification_as_read

urlpatterns = [
    path('notifications/', get_notifications, name='notifications'),
    path('mark_notification_as_read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),

]