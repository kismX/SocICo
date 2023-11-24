from django.db import models
# from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from PIL import Image

class CustomUser(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=60)


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)       # geht auch
    bio = models.TextField(blank=True)
    interests = models.TextField(blank=True, help_text='Gib interessen getrennt durch Komma an')
    # user_img = models.ImageField(upload_to='user_img/', blank=True)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')

    def __str__(self):
        return self.user.username
    
    # Having large images saved only to show a scaled/smaller version of it on the profile page might cause our app to run slow. 
    # We can mitigate this problem by using pillow to resize the large image and override it with the resized/smaller image.
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
    

