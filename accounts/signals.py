from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import Profile
from .views import update_activity_status

@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=get_user_model())
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    update_activity_status(user.profile)

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    update_activity_status(user.profile)

