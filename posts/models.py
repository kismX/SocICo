from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image

class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    event = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(get_user_model(), related_name='likes', blank=True)
    
    # bildgröße auf 500x500 begrenzen, aber seitenverhältnisse beibehalten
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.image.path)
    
    # wir zählen die likes
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Post von {self.user.username}"



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.TextField()
    image = models.ImageField(upload_to='comment_images', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(get_user_model(), related_name='like_comment', blank=True)

    # bildgröße auf 300x300 proportional begrenzt
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
    
    def total_likes_comment(self):
        return self.likes.count()

    def __str__(self):
        return f"Kommentar von {self.user.username} auf Post {self.post.id}"



class Event(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images', blank=True, null=True)

    def __str__(self):
        return self.title