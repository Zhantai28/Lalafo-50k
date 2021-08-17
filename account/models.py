from django.db import models
from django.conf import settings

#from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
      
    userbirth = models.DateField(db_column='userBirth', blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(blank=True, null=True, upload_to='profile_photo')
    region = models.CharField(max_length=1, choices=(
        ('B', 'Bishkek'),
        ('C', 'Chuy'),
        ('I', 'Issyk-Kul'),
        ('N', 'Naryn'),
        ('T', 'Talas'),
        ('O', 'Osh'),
        ('D', 'Djalal-Abad'),
        ('A', 'Batken'),
    ))
    city =models.CharField(max_length=255)



    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)