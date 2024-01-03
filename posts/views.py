from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import PostForm, CommentForm, EventForm
from basics.utils import get_domain

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
    return render(request, 'edit_comment.html', {'form': form})


# comments deleten
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)
    return render(request, 'delete_comment.html', {'comment': comment})


# liken
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    #return redirect('post_detail', post_id=post_id)
    # wir leiten den user lieber uff die seite zurück, von der er kam, damit nach like nicht auf post_detail
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



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