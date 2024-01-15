from django.contrib.auth.models import AnonymousUser
from notifications.models import Notification

def make_context_global(request):
    # wenn wir nicht ausschließen, dass ein request.user nicht unangemeldet sein kann (also Anonymous), geht alles gewaltig schief :D
    if not isinstance(request.user, AnonymousUser):
        notifications_new = Notification.objects.filter(to_user=request.user, is_read=False)
        notifications_new_count = notifications_new.count()
    else:
        notifications_new_count = None
    
    context = {
        'notifications_new_count': notifications_new_count,
    }

    return context

# mnoch überlegen, wie man das else bestückt, wenn man andere context_variablen integriert