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
    reference_id = models.IntegerField(null=True, blank=True) # für identifikation des comments

    def __str__(self):
        if self.notification_type == 'like':
            return 'Like'
        elif self.notification_type == 'post':
            return 'Post'
        elif self.notification_type == 'comment':
            return 'Kommentar'
        elif self.notification_type == 'friendrequest':
            return 'Freundschaftsanfrage'
        elif self.notification_type == 'friendrequest_accepted':
            return 'Freundschaftsanfrage angenommen'
        elif self.notification_type == 'mention':
            return 'Erwähnung'