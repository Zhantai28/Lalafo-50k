from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse





class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
      
    userbirth = models.DateField(db_column='userBirth', blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(default='default.jpg', upload_to='profile_photo')
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
    user_rated=models.ForeignKey(settings.AUTH_USER_MODEL,  related_name='given_ratings', on_delete=models.CASCADE)
    user_received=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_ratings', on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveSmallIntegerField(choices=RATE_CHOICES, verbose_name='Оценки')
   
    class Meta:
        verbose_name_plural='Ratings'
        constraints = [models.UniqueConstraint(fields=['user_rated', 'user_received'], name='one_rating_per_user')]

    def __str__(self):
        return f'{self.user_rated.username} gave {self.rating} to {self.user_received.username}' 


# Message and Chat between users

class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG,'Dialog'),
        (CHAT, 'Chat')
    )
 
    type = models.CharField(
        'Тип',
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name='Участник')
 
    def get_absolute_url(self):
        return reverse('account:messages', kwargs={'pk' : self.pk})
 
 
class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name='Чат', on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField(verbose_name='Сообщение')
    pub_date = models.DateTimeField(verbose_name='Дата сообщения', default=timezone.now)
    is_readed = models.BooleanField(verbose_name='Прочитано', default=False)
 
    class Meta:
        ordering=['pub_date']
        verbose_name ='Сообщение'
        verbose_name_plural='Сообщения'

 
    def __str__(self):
        return self.message