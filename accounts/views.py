from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UpdateUserForm, UpdateProfileForm

#password change
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

# 2023-11-22 hinzugefügt für user adden requests etc
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile, Friendship
from django.utils import timezone # für friend connecten
from django.contrib import messages # wird verwendet um meldungen durch die views oder auch verarbeitung an den user zu schicken


# erstmal alle Templates zum createn, anzeigen und editieren von profiles der user
class UserProfileListView(LoginRequiredMixin, ListView): 
    model = Profile
    template_name = 'profile_list.html'


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profile_detail.html"

    #new 2023-11-28 friends anzeigen
    def get_context_data(self, **kwargs):
        # wir rufen die super()geordnete funktion auf, und speichern sie in context, um dann den standard-context zu erweitern
        context = super().get_context_data(**kwargs)


        #Freunde des eingeloggten users:
        # wir extrahieren den eigeloggten user, der den request gesendet hat 
        user = self.request.user
        # wir filtern uns die freunde des eingeloggten users aus Friendship objekten (wo accepted_at einen value hat)
        freunde = Friendship.objects.filter(from_user=user, accepted_at__isnull=False) | Friendship.objects.filter(to_user=user, accepted_at__isnull=False)
        # offene Freundesanfrage logged in user
        freunde_ausgehend = Friendship.objects.filter(from_user=user, accepted_at__isnull=True)
        freunde_eingehend = Friendship.objects.filter(to_user=user, accepted_at__isnull=True)


        # freunde des Users, auf dessen Profil man sich befindet
        profil_user = self.object  # hole mir das aktuelle Profile-object
        profil_freunde = Friendship.objects.filter(from_user=profil_user.user, accepted_at__isnull=False) | Friendship.objects.filter(to_user=profil_user.user, accepted_at__isnull=False)



        ##### nun fügen wir dem context hinzu  ####

        # für eingeloggten user
        context['freunde'] = freunde   #freundesobjekte
        context['freunde_namelist'] = [freund.from_user.username if user != freund.from_user else freund.to_user.username for freund in freunde]  # eine liste mit den usernamen der freunde
        
        context['freund_ausgehend'] = freunde_ausgehend  # friendrequests ausgehend: objekt-queryset
        context['freund_ausgehend_namelist'] = [freund.to_user.username for freund in freunde_ausgehend] # friendrequests ausgehend: usernamen-liste

        context['freund_eingehend'] = freunde_eingehend  # friendrequest eingehend: object-queryset
        context['freund_eingehend_namelist'] = [freund.from_user.username for freund in freunde_eingehend]  # friendrequest eingehend: usernamen-liste

        context['num_freunde'] = freunde.count()    # anzahl der freunde


        # für profil-user:
        context['profil_freunde'] = profil_freunde
        context['num_profil_freunde'] = profil_freunde.count()

        return context


class UserProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = "profile_create.html"
    fields = ["bio", "interests"]   # erweitern wenn profile erweitert  # habe "user" entfernt weil es unten dfestgelegt wird in der def, damit ein user keinen ewinfluss drauf hat
    
    # diese funktion wird unter der haube immer nach der überprüfung, ob die form gültige daten enthält, aufgerufen, um die form in datenbank zu speichern .save()
    def form_valid(self, form):
        # hier überschreiben wir die funktion, indem das user-feld (form.instance.user) 
        # auf den eingeloggten user gesetzt wird - also das user-feld wird mit dem verknüft, der das profil erstellt:
        form.instance.user = self.request.user  
        # wir rufen die grundlegende funktion nochmal auf, um eben das .save() auch auszulösen nach dem überschreiben oben
        return super().form_valid(form)
    success_url = reverse_lazy("profile_list")


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "profile_edit.html"
    fields = ["user", "bio", "interests"]     #dann auch erweitern
    success_url = reverse_lazy("profile_list")


class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = "profile_delete.html"
    success_url = reverse_lazy("profile_list")



# hier ein signup 
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = 'Successfully Changed Your Password'
    success_url = reverse_lazy('profile_detail')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile is updated successfully')
            return redirect(to='profile_edit')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    
    return render(request, 'profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})
    



#2023-11-22
@login_required
def send_friend_request(request, to_user_id):    # das to_user_id kommt aus urls.py hier rein
    to_user = get_user_model().objects.get(id=to_user_id)

    # nun mal checken, ob bereits eine anfrage gibt. 
    # wenn 'from_user' = angemeldeter user und 'to_user' (übermittelte to_user_id) in friendship enthalten, gibt es true aus ...
    if Friendship.objects.filter(from_user=request.user, to_user=to_user).exists():  
        # ..ne warmmeldung geht in admin ein - muss dann an den user noch
        messages.warning(request, 'Du hast bereits ne Anfrage an den user gestellt') 
    else:
        Friendship.objects.create(from_user=request.user, to_user=to_user, status='pending')  # neu: 'status' auf pending, weil anfrage noch ausstehend
        # message geht auch ins admin
        messages.success(request, f'Deine Anfrage wurde an {to_user.username} gesendet, Dikka')  
    return redirect('profile_detail', pk=to_user_id)


@login_required
def friend_requests(request):
    incoming_requests = Friendship.objects.filter(to_user=request.user, accepted_at__isnull=True)
    outgoing_requests = Friendship.objects.filter(from_user=request.user, accepted_at__isnull=True)
    return render(request, 'friend_requests.html', {'incoming_requests': incoming_requests, 'outgoing_requests': outgoing_requests})


@login_required
def accept_reject_friend(request, friendship_id, action):   # friendship_id und action kommen wieder aus urls.py
    friendship = Friendship.objects.get(id=friendship_id)

    if action == 'accept':
        friendship.accepted_at = timezone.now()
        friendship.status = 'accepted'
        friendship.save() # save hier lassen  :D !!
    elif action == 'reject':
        friendship.delete()
    return redirect('friend_requests')


@login_required
def withdraw_friend_request(request, profile_id):
    try:
        # Freundobject raussuchen
        friend_request = Friendship.objects.get(from_user=request.user, to_user=profile_id)
        friend_request.delete()
        return redirect('profile_deteil', pk=profile_id)
    
    except Friendship.DoesNotExist:
        messages.error(request, "Die Freundschaftsanfrage existiert doch gar nicht!")
        return redirect('profile_deteil', pk=profile_id)


@login_required
def remove_friend(request, profile_id):
    user_id = request.user.id
    try:
        friendkill = Friendship.objects.get(to_user_id=profile_id, from_user_id=user_id)
        friendkill.delete()
        return redirect('profile_detail', pk=profile_id)

    except Friendship.DoesNotExist: 
        try:    
            friendkill = Friendship.objects.get(from_user_id=profile_id, to_user_id=user_id)
            friendkill.delete()
            return redirect('profile_detail', pk=profile_id)
        except Friendship.DoesNotExist:
            return redirect('profile_detail', pk=profile_id)
    
#2023-12-08
def update_activity_status(profile):
    profile.last_online = timezone.now()
    profile.save()
