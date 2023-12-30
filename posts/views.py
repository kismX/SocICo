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
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


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