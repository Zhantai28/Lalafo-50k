from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator



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


#User Rating

RATE_CHOICES=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)

class UserRating(models.Model):
    user_rated=models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='given_ratings', on_delete=models.SET_NULL)
    user_received=models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='received_ratings', on_delete=models.SET_NULL, verbose_name='Пользователь')
    rating = models.PositiveSmallIntegerField(choices=RATE_CHOICES, verbose_name='Оценки')
   
    class Meta:
        verbose_name_plural='Ratings'

    def __str__(self):
        return self.user_rated.username
