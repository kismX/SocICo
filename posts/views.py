from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, EventForm
from accounts.models import Profile

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


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


def newsfeed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


# noch hier, kommt aber in eine separate basis-app für das projekt
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

