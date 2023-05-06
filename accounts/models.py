from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager



def upload_to(instance, filename):
    print(instance.username)
    return 'static/images/{}/{}'.format(instance.username, filename)


class CustomUser(AbstractUser):
    photo = models.ImageField(
        upload_to=upload_to, blank=True, null=True, default='static/images/def/def.jpg')

    @property
    def photo_url(self):
        return self.photo.url

    def __str__(self):
        return self.username
