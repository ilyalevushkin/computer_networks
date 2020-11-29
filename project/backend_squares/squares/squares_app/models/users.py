from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True)
    photo = models.ImageField(
        upload_to='users/photo', default='users/photo/base_photo.jpg'
    )
    about = models.TextField(blank=True)

    friends = models.ManyToManyField('self', blank=True)