from django.db import models
from django.contrib.auth import get_user_model

class Notification(models.Model):
    to_user = models.ForeignKey(get_user_model(), related_name='notifications', on_delete=models.CASCADE)
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE, null=True, blank=True)
    chat_message = models.ForeignKey('chats.Message', on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=100)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_info = models.TextField()
    notification_link = models.URLField()
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification von {self.from_user} an {self.to_user} vom Typ {self.notification_type}"