from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils import timezone  # 23-11-22 für friendship
from PIL import Image


class CustomUser(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=60)


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    interests = models.TextField(blank=True, help_text='Gib interessen getrennt durch Komma an')
    # user_img = models.ImageField(upload_to='user_img/', blank=True)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')

    def __str__(self):
        return self.user.username
    

    # 2023-11-22 neu get_friends() um alle bestehenden freundschaften zu ermitteln
    # easy: ich verweise auf mein neu erstelltes model Friendship und filter mir aus den friedshipobjekten alle geaddeten raus
    def get_friends(self):
        friends = Friendship.objects.filter(accepted_at__isnull=False)
        return [friend for friend in friends] # spucke mir jeden friend in friends aus (wollt mal wieder dings hier üben.. [ ])
    
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

    

