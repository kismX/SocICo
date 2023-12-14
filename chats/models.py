from django.db import models
from django.contrib.auth import get_user_model


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug

class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)