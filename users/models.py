from django.contrib.auth.models import AbstractUser
from django.db import models

def user_avatar_path(instance, filename):
    return f'image/user_{instance.user.id}/{filename}'

class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=20, null=True, blank=True)

    image = models.ImageField(upload_to='profile_images',
                              null=True, blank=True,
                              default='profile_images/default.png',
                              verbose_name='Profile images',
                              )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['email']

    def __str__(self):
        return self.email or self.username
