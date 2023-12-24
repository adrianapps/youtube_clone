from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Channel(models.Model):
    name = models.CharField(max_length=30)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User, related_name='channel_subscribers', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='media/avatars')

    def __str__(self):
        return f"{self.name}"
