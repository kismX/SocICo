from django.contrib.auth.models import AnonymousUser
from notifications.models import Notification
from django.contrib.auth import get_user_model


def make_context_global(request):
    context = {}
    
    # wenn wir nicht ausschließen, dass ein request.user nicht unangemeldet sein kann (also Anonymous), geht alles gewaltig schief :D
    if not isinstance(request.user, AnonymousUser):
        notifications_new = Notification.objects.filter(to_user=request.user, is_read=False)
        notifications_new_count = notifications_new.count()

        context = {
            'notifications_new_count': notifications_new_count,
        }
    return context