from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .models import Notification

# für einfache notifications ohne websockets
def create_notification(to_user, from_user, notification_type, notification_info, notification_link):
    notification = Notification.objects.create(
        to_user=to_user,
        from_user=from_user,
        notification_type=notification_type,
        notification_info=notification_info,
        notification_link=notification_link,
        is_sent=False
    )
    return notification


def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(to_user=request.user, is_read=False)
        return render(request, 'notifications.html', {'notifications': notifications})
    else:
        return HttpResponse("Nicht authentifiziert.")
    

@require_POST
def mark_as_read(request):
    notification_id = request.POST.get('notification_id')
    try:
        notification = Notification.objects.get(id=notification_id, to_user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)


def get_unsent_notifications(request):
    if request.user.is_authenticated:
        unsent_notifications = Notification.objects.filter(
            to_user=request.user, 
            is_sent=False
        ).values() 

        # notifications als gesendet markieren
        unsent_notifications.update(is_sent=True)

        return JsonResponse({"notifications": list(unsent_notifications)})
    else:
        return JsonResponse({"error": "Nicht authentifiziert"}, status=401)