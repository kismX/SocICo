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
    
    # bildgröße auf 500x500 begrenzen, aber seitenverhältnisse beibehalten
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.image.path)
    
    def __str__(self):
        return f"Post von {self.user.username}"



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