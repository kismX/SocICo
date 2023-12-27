from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UpdateUserForm, UpdateProfileForm
from posts.models import Post # für post anzeigen des users auf profile_detail
from posts.forms import PostForm
from basics.utils import get_domain

# 2023-11-22 hinzugefügt für user adden requests etc
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile, Friendship
from django.utils import timezone # für friend connecten
from django.contrib import messages # wird verwendet um meldungen durch die views oder auch verarbeitung an den user zu schicken


# erstmal alle Templates zum createn, anzeigen und editieren von profiles der user
class UserProfileListView(LoginRequiredMixin, ListView): 
    model = Profile
    template_name = 'profile/profile_list.html'


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profile/profile_detail.html"

    #new 2023-11-28 friends anzeigen
    def get_context_data(self, **kwargs):
        # wir rufen die super()geordnete funktion auf, und speichern sie in context, um dann den standard-context zu erweitern
        context = super().get_context_data(**kwargs)

        #Freunde des eingeloggten users:
        user = self.request.user
        freunde = Friendship.objects.filter(from_user=user, accepted_at__isnull=False) | Friendship.objects.filter(to_user=user, accepted_at__isnull=False)
        
        # offene Freundesanfrage logged in user
        freunde_ausgehend = Friendship.objects.filter(from_user=user, accepted_at__isnull=True)
        freunde_eingehend = Friendship.objects.filter(to_user=user, accepted_at__isnull=True)

        # freunde des Users, auf dessen Profil man sich befindet
        profil_user = self.object  # hole mir das aktuelle Profile-object
        profil_freunde = Friendship.objects.filter(from_user=profil_user.user, accepted_at__isnull=False) | Friendship.objects.filter(to_user=profil_user.user, accepted_at__isnull=False)

        freund_profil = Friendship.objects.filter(from_user=profil_user.user, to_user=user, accepted_at__isnull=False).first() or Friendship.objects.filter(to_user=profil_user.user, from_user=user, accepted_at__isnull=False).first()
        if freund_profil:
            freund_seit = freund_profil.accepted_at
        else:
            freund_seit = None

        # timeline aus postings auf der profilseite anzeigen
        profile_user_posts = Post.objects.filter(user=profil_user.pk).order_by('-created_at')  # post-obj des profilusers
        user_posts = Post.objects.filter(user=user).order_by('-created_at') # post-obj des request-users
        
        # wenn in einem objekt ein link ist, hole über get_domain die URL 
        # und füge sie in einem neuen attribut .domain dem post.objekt hinzu
        # wodurch post.domain im template abrufbar wird
        for post in profile_user_posts:
            if post.link:
                post.domain = get_domain(post.link)


        ##### nun fügen wir dem context hinzu  ####

        # für eingeloggten user
        context['freunde'] = freunde   #freundesobjekte
        context['freunde_namelist'] = [freund.from_user.username if user != freund.from_user else freund.to_user.username for freund in freunde]  # eine liste mit den usernamen der freunde
        
        context['freund_ausgehend'] = freunde_ausgehend  # friendrequests ausgehend: objekt-queryset
        context['freund_ausgehend_namelist'] = [freund.to_user.username for freund in freunde_ausgehend] # friendrequests ausgehend: usernamen-liste

        context['freund_eingehend'] = freunde_eingehend  # friendrequest eingehend: object-queryset
        context['freund_eingehend_namelist'] = [freund.from_user.username for freund in freunde_eingehend]  # friendrequest eingehend: usernamen-liste

        context['num_freunde'] = freunde.count()    # anzahl der freunde
        if freund_profil:
            context['freund_seit'] = freund_seit        # seit wann befreundet

        # für profil-user:
        context['profil_freunde'] = profil_freunde
        context['num_profil_freunde'] = profil_freunde.count()

        # posts des users auf profil
        context['user_posts'] = user_posts
        context['profile_user_posts'] = profile_user_posts

        # wenn benutzer auf seinem eigenen profil, dann kann er posten:
        #if user == profil_user:
        context['post_form'] = PostForm()
        
        return context


class UserProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = "profile/profile_create.html"
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
    template_name = "profile/profile_delete.html"
    success_url = reverse_lazy("profile_list")


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        profile_instance = Profile.objects.get(id=request.user.id)

        if user_form.is_valid() and profile_form.is_valid():
            
            # altes bild durch neues ersetzen:
            new_image = request.FILES.get('avatar')
            old_image = getattr(profile_instance, 'avatar')
            
            if new_image == None:
                profile = profile_form.save(commit=False)
                profile.save(update_fields=['age', 'gender', 'location', 'bio', 'interests'])
            elif old_image == 'default.jpg':
                profile_form.save()
            else:
                old_image.delete()
                profile_form.save()

            user_form.save()
            messages.success(request, 'Your Profile is updated successfully')
            return redirect(to='profile_detail', pk=request.user.id)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    
    return render(request, 'profile/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})
    

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
    return render(request, 'profile/friend_requests.html', {'incoming_requests': incoming_requests, 'outgoing_requests': outgoing_requests})


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
    

def update_activity_status(profile):
    profile.last_online = timezone.now()
    profile.save(update_fields=['last_online'])


#2023-12-16 - user nur für freude sichtbar
def invisible_check(request):
    user = request.user.id
    profil = request.user.profile

    #wennn im request.POST ein wert für 'invisible' enthalten ist (ckeckbox gehakt), dann führe aus:
    if 'invisible' in request.POST:
        profil.invisible = True
    else:
        profil.invisible = False

    profil.save()
    return redirect('profile_detail', pk=user)

