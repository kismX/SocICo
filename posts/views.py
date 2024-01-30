from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, JsonResponse

from .models import Post, Comment
from notifications.models import Notification
from .forms import PostForm, CommentForm, EventForm
from basics.utils import get_domain
from accounts.models import Profile

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from notifications.views import delete_notifications, create_notification, mention_users_in_text

# views zum posten
def create_post(request, profile_id=None):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # verknüpft den post mit einem profile eindeutig
            profile_id = request.POST.get('profile_id')
            post.profile = get_object_or_404(Profile, id=profile_id) if profile_id else request.user.profile
            post.user = request.user

            # show_in_feed abhängig des profils
            if str(request.user.profile.id) == profile_id:
                post.show_in_feed = form.cleaned_data.get('show_in_feed', False)
            else:
                post.show_in_feed = False

            post.save()

            # nun durch die mention-funktion schicken
            post.text = mention_users_in_text(request, post.text, post)
            post.save()

            # notification erstellen
            profile_owner = get_object_or_404(Profile, id=profile_id) if profile_id else request.user.profile
            if request.user != profile_owner.user:
                notification_info = f"{request.user.username} hat einen neuen Beitrag auf deinem Profil erstellt."
                notification_link = f"/posts/post/{post.id}/"
                reference_id = post.id
                print("profile:", profile_owner.user)
                create_notification(profile_owner.user, request.user, 'post', notification_info, notification_link, reference_id)
            
            #return redirect('profile_detail', pk=post.user.id)
            return redirect('profile_detail', pk=profile_id if profile_id else post.user.id)
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', pk=post.user.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form})


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        reference_id = post.id
        delete_notifications(post.user, request.user, 'post', post, reference_id)
        post.delete()
        return redirect('profile_detail', pk=post.user.id)
    return render(request, 'posts/delete_post.html', {'post': post})


# für einzelne posts auf profile_detail
@login_required
@require_POST
def update_post_feed(request):
    post_id = request.POST.get('post_id')
    show_in_feed = request.POST.get('show_in_feed') == 'true'

    post = get_object_or_404(Post, id=post_id, profile=request.user.profile)
    post.show_in_feed = show_in_feed
    post.save()

    return JsonResponse({'status': 'success'})


# für alle posts über profile_settings
# @login_required
# @require_POST
# def update_all_posts_feed(request):
#     show_in_feed = request.POST.get('show_in_feed') == 'true'
   
#     # Aktualisiere alle Posts des aktuellen Benutzers auf den angegebenen Feed-Status
#     posts = Post.objects.filter(profile=request.user.profile)
#     for post in posts:
#         post.show_in_feed = show_in_feed
#         post.save()
    
#     return JsonResponse({'status': 'success'})


# comments auf post schicken:
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    # alle comments-Objekte, deren post-field gleich dem in z41 def post-Objekt ist:
    comments = Comment.objects.filter(post=post) 

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        # hierdurch wird auch die clean() method in MOdel aktiv (auch im hintergrund, wenn wir sie nicht angepasst hätten):
        if comment_form.is_valid(): 
            comment = comment_form.save(commit=False) # erstellen instanzobjekt, speichern es nicht ab, weil Foreign_verbindungen fehlen
            comment.post = post # verknüfen nun mit post aus post Modell mit der aktuellen post_id
            comment.user = request.user # verknüpfen mit aktuellem request.user aus CustomUser modell
            comment.save() # jetzt speichern wir das objekt angepasst in database

            # nun in die mention-funktion für erwähnung
            #comment.comment = mention_users_in_text(request, comment.comment, None, comment)
            comment.comment = mention_users_in_text(request, comment.comment, comment)
            comment.save()

            # notification erstellen ohne websockets
            if post.user != request.user:
                notification_info = f"{request.user.username} hat deinem Beitrag einen Kommentar hinzugefügt."
                notification_link = f"/posts/post/{post.id}/"
                reference_id=comment.id
                create_notification(post.user, request.user, 'comment', notification_info, notification_link, reference_id)
         
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'posts/post_detail.html', context)


# comments editieren
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        # wir erstellen ein CommentForm Objekt "form", 
        # welches den user-request aus dem "request.POST" und dem aktuellen comment enthält
        # 'instance' ist n parameter, der in der Klasse ModelForm enthalten ist. 
        # den man aufruft und mit einem Instanzobjekt dieser CommentForm verknüpft, 
        # was in diesem Fall "comment" aus z.69 ist, welches mit dem Comment-Objekt 
        # verbunden ist, das die id=comment_id hat
        # mit form.save() überschreiben wir den gewünschten comment dann:
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'posts/comment_edit.html', {'form': form})


# comments deleten
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        reference_id = comment.id
        delete_notifications(comment.post.user, request.user, 'comment', comment, reference_id)
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)
    return render(request, 'posts/comment_delete.html', {'comment': comment})


# OHNE WEBSOCKETS VERSIONs
def like_post_ajax(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        reference_id=post.id
        delete_notifications(post.user, request.user, 'like', post, reference_id)
    else:
        post.likes.add(request.user)
        liked = True

        # Benachrichtigung erstellen, wenn Post geliked wird
        if post.user != request.user:
            notification_info = f"{request.user.username} hat deinen Beitrag geliked."
            notification_link = f"/posts/post/{post.id}/"
            reference_id = post.id
            create_notification(post.user, request.user, 'like', notification_info, notification_link, reference_id)

    return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})


def like_comment_ajax(request):
    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, id=comment_id)
    liked = False

    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        reference_id=comment.id
        delete_notifications(comment.user, request.user, 'like', comment, reference_id)

    else:
        comment.likes.add(request.user)
        liked = True

        # Benachrichtigung erstellen, wenn Kommentar geliked wird
        if comment.user != request.user:
            notification_info = f"{request.user.username} hat deinen Kommentar geliked."
            notification_link = f"/posts/post/{comment.post.id}/"
            reference_id = comment.id
            create_notification(comment.user, request.user, 'like', notification_info, notification_link, reference_id)            

    return JsonResponse({'liked': liked, 'total_likes_comment': comment.total_likes_comment()})


# liste der user , die geliked haben auf like_list.html
def like_list_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_user_likes = post.likes.all()
    return render(request, 'posts/like_list.html', {'post_user_likes': post_user_likes, 'post': post})
 
def like_list_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment_user_likes = comment.likes.all()
    return render(request, 'posts/like_list.html', {'comment_user_likes': comment_user_likes, 'comment': comment})
 




# views zu events - bald
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()

            Post.objects.create(user=request.user, event=event, text=event.description)

            return redirect('newsfeed')
    else:
        form = EventForm()
    return render(request, 'posts/create_event.html', {'form': form})