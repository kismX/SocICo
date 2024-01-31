from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from datetime import date
#from PIL import Image


class CustomUser(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=60)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True)
    birthdate = models.DateField(default=timezone.datetime(1955, 2, 24), null=False, blank=False)


class Profile(models.Model):
    GENDER_CHOICES = [
        ('female', 'weiblich'),
        ('male', 'männlich'),
        ('divers', 'divers'),
    ]
    
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True) 
    bio = models.TextField(blank=True)
    interests = models.TextField(blank=True, help_text='Gib interessen getrennt durch Komma an')
    avatar = models.ImageField(default='default.png', upload_to='profile_images')
    is_active = models.BooleanField(default=False)  # ist er geraed online oder offline - muss noch implementiert weden
    chat_status = models.BooleanField(default=False)
    last_online = models.DateTimeField(blank=True, null=True)  # wann war user letztes mal online
    invisible = models.BooleanField(default=False) # user invisible mode für nicht-freunde

    # attribute für sichtbarkeit von profilinfos, default ist sichtbar:
    birthdate_visible = models.BooleanField(default=True)
    age_visible = models.BooleanField(default=True)
    gender_visible = models.BooleanField(default=True)
    country_visible = models.BooleanField(default=True)
    city_visible = models.BooleanField(default=True)
    bio_visible = models.BooleanField(default=True)
    interests_visible = models.BooleanField(default=True)


    def interest_list(self):
        return [interest.strip().lower() for interest in self.interests.split(',')] if self.interests else []
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):

        super(Profile, self).save(*args, **kwargs)

# neues model das eine Friednship darstellt
# es hat den 'from_user', von dem die anfrage ausgeht und 'to_user' an den die anfrage geht
# wann  die verbindung erstellt wurde geht automatisch: 'createtd_at' und wenn request angenommen, wird das leere 'acceptet_at' mit zeitpunkt ausgefüllt
class Friendship(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ausstehend'),
        ('accepted', 'Akzeptiert'),
        ('rejected', 'Abgelehnt'),
        ('withdrawn', 'Zurückgezogen'),
    )
    
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='to_user')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=30, default='pending')  # hjier wird jeweils der status gespeichert nach requests, accepts.. usw

    # lasse mir die beziehung zwischen sender und empfänger der freundschaft und deren status ()ausgeben - objekt einfacher zu lesen
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})" 

    

