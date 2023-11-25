from django.shortcuts import render

# 2023-11-22 hinzugefügt für user adden requests etc
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Friendship
from django.utils import timezone # für friend connecten
from django.contrib import messages # wird verwendet um meldungen durch die views oder auch verarbeitung an den user zu schicken


#2023-11-22
#Friend Request stellen
@login_required
def send_friend_request(request, to_user_id):    # das to_user_id kommt aus urls.py hier rein
    to_user = get_user_model().objects.get(id=to_user_id)

    # nun mal checken, ob bereits eine anfrage gibt. 
    # wenn 'from_user' = angemeldeter user und 'to_user' (übermittelte to_user_id) in friendship enthalten, gibt es true aus ...
    if Friendship.objects.filter(from_user=request.user, to_user=to_user).exists():  
        # ..ne warmmeldung geht in admin ein - muss dann an den user noch
        messages.warning(request, 'Du hast bereits ne Anfrage an den user gestellt') 
    else:
        Friendship.objects.create(from_user=request.user, to_user=to_user)
        # message geht auch ins admin
        messages.success(request, f'Deine Anfrage wurde an {to_user.username} gesendet, Dikka')  
    return redirect('profile_detail', pk=to_user_id)


# Anzeigen von Friend-requests
@login_required
def friend_requests(request):
    incoming_requests = Friendship.objects.filter(to_user=request.user, accepted_at__isnull=True)
    outgoing_requests = Friendship.objects.filter(from_user=request.user, accepted_at__isnull=True)
    return render(request, 'friend_requests.html', {'incoming_requests': incoming_requests, 'outgoing_requests': outgoing_requests})


# nun akzeptieren und ablehnen der freundschaftsanfragen
@login_required
def accept_reject_friend(request, friendship_id, action):   # friendship_id und action kommen wieder aus urls.py
    friendship = Friendship.objects.get(id=friendship_id)

    if action == 'accept':
        friendship.accepted_at = timezone.now()
        friendship.save() # save hier lassen  :D !!
    elif action == 'reject':
        friendship.delete()
    
 
    return redirect('friend_requests')