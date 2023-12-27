from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Channel(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    description = models.TextField(max_length=5000, blank=True)
    subscribers = models.ManyToManyField(User, related_name='channel_subscribers', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='media/avatars')

    @property
    def subscriber_count(self):
        return self.subscribers.count()

    def subscription_status(self, user):
        return self.subscribers.filter(pk=user.id).exists()

    def __str__(self):
        return self.name
