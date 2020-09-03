from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm

# Create your models here.
# from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name='first name')
    last_name = models.CharField(max_length=100, verbose_name='last name')
    def __str__(self):
        return self.username
    image_user = models.ImageField(null = True, blank = True, upload_to = 'news/profile_image/')
    @property
    def image_url(self):
        if self.image_user:
            return self.image_user
        
