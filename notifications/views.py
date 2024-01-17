from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
import re  
from .models import Notification
from posts.models import Comment


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
        notifications_new = Notification.objects.filter(to_user=request.user, is_read=False).order_by('-created_at')
        notifications_read = Notification.objects.filter(to_user=request.user, is_read=True).order_by('-created_at')
        return render(request, 'notifications/notifications.html', {'notifications_new': notifications_new, 'notifications_read': notifications_read})
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


# user erwähnen
def mention_users_in_text(request, text, target):
    user = get_user_model()
    pattern = r'@(\w+)' # finde @ und suche alphanumerische zeichenketten mit mind 1 zeichen
    mentioned_users = re.findall(pattern, text) #re modul und das findall sucht eben nach diesen zeichenketten und mach in liste

    # Ersetze usernamen in Text durch Links zu den Profilen
    for username in mentioned_users:
        user = user.objects.filter(username=username).first()
        if user:
            profile_link = reverse('profile_detail', args=[user.id])
            text = text.replace(f'@{username}', f'<a href="{profile_link}"><strong>{username}</strong></a>')
            
            # Erstelle notification für erwähnten userrr
            if user != request.user and target:                 
                if isinstance(target, Comment):
                    notification_info = f"{request.user.username} hat dich in einem Kommentar erwähnt."
                    notification_link = f"/posts/post/{target.post.id}/"
                else:  # Falls target n Post ist 
                    notification_info = f"{request.user.username} hat dich in einem Post erwähnt."
                    notification_link = f"/posts/post/{target.id}/"
                create_notification(user, request.user, 'mention', notification_info, notification_link)
    
    return text
