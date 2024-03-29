from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from .forms import UpdateUserForm, UpdateProfileForm
from posts.models import Post
from posts.forms import PostForm
from basics.utils import get_domain

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile, Friendship
from django.utils import timezone 
from django.contrib import messages 
from django.shortcuts import get_object_or_404
from PIL import Image
from datetime import date
# für Ajax invisible_check
from django.views.decorators.http import require_POST
from notifications.views import create_notification, delete_notifications
from django.http import JsonResponse

from cities_light.models import City

def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})

# erstmal alle Templates zum createn, anzeigen und editieren von profiles der user
class UserProfileListView(LoginRequiredMixin, ListView): 
    model = Profile
    template_name = 'profile/profile_list.html'


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profile/profile_detail.html"

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
        list_of_friends = []

        for friend_obj in profil_freunde:
            if friend_obj.from_user != profil_user.user:
                list_of_friends.append(friend_obj.from_user)
            else:
                list_of_friends.append(friend_obj.to_user)


        freund_profil = Friendship.objects.filter(from_user=profil_user.user, to_user=user, accepted_at__isnull=False).first() or Friendship.objects.filter(to_user=profil_user.user, from_user=user, accepted_at__isnull=False).first()
        if freund_profil:
            freund_seit = freund_profil.accepted_at
        else:
            freund_seit = None

        # age berechnen
        today = date.today()
        age = today.year - profil_user.user.birthdate.year - ((today.month, today.day) < (profil_user.user.birthdate.month, profil_user.user.birthdate.day))

        # timeline aus postings auf der profilseite anzeigen
        #profile_user_posts = Post.objects.filter(user=profil_user.pk).order_by('-created_at')  # post-obj des profilusers
        profile_user_posts = Post.objects.filter(profile=profil_user).order_by('-created_at')  # post-obj des verknpften profils
        user_posts = Post.objects.filter(user=user).order_by('-created_at') # post-obj des request-users
        
        # wenn link im post-objekt, erstelle post.domain attribut und speichewr darin über get_domain die URL
        for post in profile_user_posts:
            if post.link:
                post.domain = get_domain(post.link)

        ##### nun fügen wir dem context hinzu  ####
        context.update({
            'profile_id': self.kwargs.get('pk'),
            'freunde': freunde,   #freundesobjekte
            'freunde_namelist': [freund.from_user.username if user != freund.from_user else freund.to_user.username for freund in freunde], # eine liste mit den usernamen der freunde
            'freund_ausgehend': freunde_ausgehend, # friendrequests ausgehend: objekt-queryset
            'freund_ausgehend_namelist': [freund.to_user.username for freund in freunde_ausgehend],   # friendrequests ausgehend: usernamen-liste
            'freund_eingehend': freunde_eingehend,
            'freund_eingehend_namelist': [freund.from_user.username for freund in freunde_eingehend],
            'num_freunde': freunde.count(),    # anzahl der freunde
            'age': age,
            
            # für profil-user:
            'profil_freunde': list_of_friends,
            'num_profil_freunde': profil_freunde.count(),
            # posts des users auf profil:
            'user_posts': user_posts,
            'profile_user_posts': profile_user_posts,
            # wenn benutzer auf seinem eigenen profil, dann kann er posten:
            'post_form': PostForm(),
        })

        if freund_profil:
            context['freund_seit'] = freund_seit   # seit wann befreundet
        
        return context


class UserProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = "profile/profile_create.html"
    fields = ["bio", "interests"] # habe "user" entfernt weil es unten festgelegt wird in der def, damit ein user keinen einfluss drauf hat
    
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
    fields = ["user", "bio", "interests",]     #dann auch erweitern
    success_url = reverse_lazy("profile_list")


class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = "profile/profile_delete.html"
    success_url = reverse_lazy("profile_list")


@login_required
def profile(request):

    # Verarbeitet Profilbearbeitung

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
                profile.save(update_fields=['gender', 'bio', 'interests'])
            elif old_image == 'default.png':
                profile_form.save()
                my_profile = Profile.objects.get(id=request.user.id)
                img = Image.open(my_profile.avatar.path)
                if img.height > 200 or img.width > 200:
                    new_img = (200, 200)
                    img.thumbnail(new_img)
                    img.save(my_profile.avatar.path)
            else:
                old_image.delete()
                profile_form.save()
                my_profile = Profile.objects.get(id=request.user.id)
                img = Image.open(my_profile.avatar.path)
                if img.height > 200 or img.width > 200:
                    new_img = (200, 200)
                    img.thumbnail(new_img)
                    img.save(my_profile.avatar.path)

            user_form.save()
            messages.success(request, 'Your Profile is updated successfully')
            return redirect(to='profile_detail', pk=request.user.id)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    return render(request, 'profile/profile_edit.html', context)
    

@login_required
def send_friend_request(request, to_user_id):
    to_user = get_object_or_404(get_user_model(), id=to_user_id)

    # nun mal checken, ob bereits eine anfrage gibt. 
    # wenn 'from_user' = angemeldeter user und 'to_user' (übermittelte to_user_id) in friendship enthalten, gibt es true aus ...
    if Friendship.objects.filter(from_user=request.user, to_user=to_user).exists():  
        messages.warning(request, 'Du hast bereits ne Anfrage an den user gestellt') 
    else:
        friendship = Friendship.objects.create(from_user=request.user, to_user=to_user, status='pending')  # neu: 'status' auf pending, weil anfrage noch ausstehend
        #notification erstellen:
        notification_info = f"{request.user.username} schickt dir eine Freundschaftsanfrage."
        notification_link = f"/accounts/friend_requests/"
        reference_id = friendship.id
        create_notification(friendship.to_user, friendship.from_user, 'friendrequest', notification_info, notification_link, reference_id)
        messages.success(request, f'Deine Anfrage wurde an {to_user.username} gesendet, Dikka')  
    return redirect('profile_detail', pk=to_user_id)


@login_required
def friend_requests(request):
    incoming_requests = Friendship.objects.filter(to_user=request.user, accepted_at__isnull=True)
    outgoing_requests = Friendship.objects.filter(from_user=request.user, accepted_at__isnull=True)
    return render(request, 'profile/friend_requests.html', {'incoming_requests': incoming_requests, 'outgoing_requests': outgoing_requests})


@login_required
def accept_reject_friend(request, friendship_id, action):
    friendship = Friendship.objects.get(id=friendship_id)

    if action == 'accept':
        friendship.accepted_at = timezone.now()
        friendship.status = 'accepted'
        friendship.save()
        # Benachrichtigung wenn akzeptiert:
        notification_info = f"{friendship.from_user.username} hat deine Freundschaftsanfrage akzeptiert."
        notification_link = f"/accounts/profiles/{friendship.to_user.id}"
        create_notification(friendship.from_user, friendship.to_user, 'friendrequest_accepted', notification_info, notification_link)
    elif action == 'reject':
        friendship.delete_notifications()
        friendship.delete()
    return redirect('friend_requests')


@login_required
def withdraw_friend_request(request, profile_id):
    try:
        # Freundobject raussuchen
        friend_request = Friendship.objects.get(from_user=request.user, to_user=profile_id)
        reference_id=friend_request.id
        delete_notifications(friend_request.to_user, friend_request.from_user, 'friendrequest', reference_id)
        friend_request.delete()
        return redirect('profile_deteil', pk=profile_id)
    
    except Friendship.DoesNotExist:
        messages.error(request, "Die Freundschaftsanfrage existiert doch gar nicht!")
        return redirect('profile_detail', pk=profile_id)


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


@login_required
@require_POST
def invisible_check(request):
    profil = request.user.profile
    profil.invisible = not profil.invisible
    profil.save()
    
    return JsonResponse({'visible': profil.invisible})


# views für Template profile_settings
@login_required
def profile_settings(request):
    # Hier kannst du auf das Profilobjekt des aktuellen Benutzers zugreifen
    profile = request.user.profile
    # Füge den Code für die Anzeige und Bearbeitung der Einstellungen hinzu
    return render(request, 'profile/profile_settings.html', {'profile': profile})


def toggle_profile_visibility(request, toggle_type):
    if request.method == 'POST':
        profile = request.user.profile
        
        if toggle_type in ['birthdate', 'age', 'country', 'city', 'gender', 'bio', 'interests']:
            setattr(profile, toggle_type + '_visible', not getattr(profile, toggle_type + '_visible'))
        
        profile.save()
        return JsonResponse({'visible': getattr(profile, toggle_type + '_visible')})
    return JsonResponse({'error': 'Invalid request'})
