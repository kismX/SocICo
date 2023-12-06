from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from PIL import Image


class CustomUser(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=60)


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    interests = models.TextField(blank=True, help_text='Gib interessen getrennt durch Komma an')
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')

    def __str__(self):
        return self.user.username
    
    # Große des Images auf 100x00 skalieren mit library pillow
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


# neues model das eine Friednship darstellt
# es hat den 'from_user', von dem die anfrage ausgeht und 'to_user' an den die anfrage geht
# wann  die verbindung erstellt wurde geht automatisch: 'createtd_at' und wenn request angenommen, wird das leere 'acceptet_at' mit zeitpunkt ausgefüllt
class Friendship(models.Model):
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='to_user')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    

