from django.contrib.auth.models import User
from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)



