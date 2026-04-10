from django.db import models

# Create your models here.

class Profil(models.Model):
    avatar = models.ImageField(upload_to='profile_pics')