from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Notification

def create_notification(to_user, from_user, notification_type, notification_info, notification_link):
    notification = Notification.objects.create(
        to_user=to_user,
        from_user=from_user,
        notification_type=notification_type,
        notification_info=notification_info,
        notification_link=notification_link,
        #is_sent=False
    )
    return notification


def get_notifications(request):
    if request.user.is_authenticated:
        notifications_new = Notification.objects.filter(to_user=request.user, is_read=False)
        notifications_read = Notification.objects.filter(to_user=request.user, is_read=True)
        return render(request, 'notifications.html', {'notifications_new': notifications_new, 'notifications_read': notifications_read})
    else:
        return HttpResponse("Nicht authentifiziert.")


def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, to_user=request.user)
    
    # wenn notification, hole url zum redirecten und  notification = is_read
    if notification:
        target_url = notification.notification_link
        notification.is_read = True
        notification.save()
    
    return redirect(target_url)