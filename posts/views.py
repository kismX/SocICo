from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse

from .models import Post, Comment
from notifications.models import Notification
from .forms import PostForm, CommentForm, EventForm
from basics.utils import get_domain

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# views zum posten
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('profile_detail', pk=post.user.id)
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
        post.delete()
        return redirect('profile_detail', pk=post.user.id)
    return render(request, 'posts/delete_post.html', {'post': post})

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
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)
    return render(request, 'posts/comment_delete.html', {'comment': comment})


# liken (ajax)
# + notification wenn like
def like_post_ajax(request):  # signal websocket läuft!
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True

        # Erstelle notification nur, wenn Post-ersteller und likender User unterschiedlich sind
        if post.user != request.user:
            notification = Notification.objects.create(
                to_user=post.user,
                from_user=request.user,
                post=post,
                notification_type='like',
                notification_info=f"{request.user.username} hat deinen Post geliked.",
                notification_link=f"/post/{post.id}/",
                is_sent = False # hinzugefügt
            )
            print(f"Notification für Post erstellt: {notification.id} für {notification.to_user}") #test funktioniert!!
            
            # Senden der notifications über channels
            channel_layer = get_channel_layer()
            group_name = f"notification_user_{post.user.id}"
            print(f"Senden an Grouououp: {group_name}")  # test funktioniert

            async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "message": {
                    "notification_id": notification.id,
                }
            }
        )
        print(f"Nachricht gesendet für Notifiation post: {notification.id}")  #test funktioniert

    return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})


def like_comment_ajax(request): # signal websocket läuft!
    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, id=comment_id)
    liked = False

    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
        liked = True

        if comment.user != request.user:
            notification = Notification.objects.create(
                to_user=comment.user,
                from_user=request.user,
                comment=comment,
                notification_type='like',
                notification_info=f"{request.user.username} hat deinen Kommentar geliked.",
                notification_link=f"/post/{comment.post.id}/",
                is_sent = False # hinzugefügt
            )
            print(f"Notification für comment erstellt: {notification.id} für {notification.to_user}") #test funktioniert


            channel_layer = get_channel_layer()
            group_name = f"notification_user_{comment.user.id}"
            print(f"Senden an Grouououp comment : {group_name}")  # test funktioniert

            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "send_notification",
                    "message": {
                        "notification_id": notification.id,
                    }
                }
            )
            print(f"Nachricht gesendet für Notifiation comment: {notification.id}")  #test

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
 




# views zu events
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