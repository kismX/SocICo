from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import Profile

# 2023-11-22 hinzugrfügt für user adden requests etc
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Friendship
from django.utils import timezone
from django.contrib import messages # wird verwendet um meldungen durch die views oder auch verarbietung an den user zu schicken
# from django.http import JsonResponse



# erstmal alle Templates zum createn, anzeigen und editieren von profiles der user
class UserProfileListView(ListView): 
    model = Profile
    template_name = 'profile_list.html'


class UserProfileDetailView(DetailView):
    model = Profile
    template_name = "profile_detail.html"



#2023-11-23
class UserProfileCreateView(CreateView):
    model = Profile
    template_name = "profile_create.html"
    fields = ["user", "bio", "interests"]   # ändern
    success_url = reverse_lazy("profile_list")

class UserProfileUpdateView(UpdateView):
    model = Profile
    template_name = "profile_edit.html"
    fields = ["user", "bio", "interests"]     #ändern
    success_url = reverse_lazy("profile_list")

class UserProfileDeleteView(DeleteView):
    model = Profile
    template_name = "profile_delete.html"
    success_url = reverse_lazy("profile_list")




# hier ein signup 
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'



#2023-11-22
#Friend Request stellen
@login_required
def send_friend_request(request, to_user_id):    # das to_user_id kommt aus urls.py
    to_user = get_user_model().objects.get(id=to_user_id)

    # nun mal checken, ob bereits anfrage gibt. 
    if Friendship.objects.filter(from_user=request.user, to_user=to_user).exists():  # from_user ist der aktuelle user .. und ist to_user (der user mit der übermittelten id) in friendship enthalten als reuqest oder freund, gibt es true aus ...
        messages.warning(request, 'Du hast bereits ne Anfrage an den user gestellt') # ..und warmmeldung geht in admin ein - muss iwie an user noch
    else:
        Friendship.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, f'Deine Anfrage wurde an {to_user.username} gesendet, Dikka')  # message geht auch ins admin
    
    return redirect('profile_detail', pk=to_user_id)


# Anzeigen von Friend-requests
@login_required
def friend_requests(request):
    incoming_requests = Friendship.objects.filter(to_user=request.user, accepted_at__isnull=True)
    outgoing_requests = Friendship.objects.filter(from_user=request.user, accepted_at__isnull=True)

    return render(request, 'friend_requests.html', {'incoming_requests': incoming_requests, 'outgoing_requests': outgoing_requests})




# nun akzeptieren und ablehnen der freundschaftsanfragen
@login_required
def accept_reject_friend(request, friendship_id, action):   # friendship_id udn action kommen aus  urls.py
    friendship = Friendship.objects.get(id=friendship_id)

    if action == 'accept':
        friendship.accepted_at = timezone.now()
    elif action == 'reject':
        friendship.delete()
    
    friendship.save()
    return redirect('friend_requests')








# hinzufügen von friends - ohne anfrage, eigtl unsinn - war erster versuch
# @login_required
# def add_friends(request, friend_id):
#     user = request.user
#     friend = get_user_model().objects.get(id=friend_id)

#     # prüfen wir mal ob freundschaft bereits besteht
#     if not Friendship.objects.filter(from_user=user, to_user=friend).exists():
#         Friendship.objects.filter(from_user=user, to_user=friend)
#         return JsonResponse({'status': 'error', 'message': f'{friend.username} wurde hinzugefügt'})
#     else:
#         return JsonResponse({'status': 'accept', 'message': f'{friend.username} ist schon mit dir connected'})



