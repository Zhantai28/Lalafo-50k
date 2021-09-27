from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from products.models import Product
from django.db.models import Max, Count, Avg
from django.core.validators import MaxValueValidator, MinValueValidator






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


    def averagerating(self):
        ratings = UserRating.objects.filter(user_received=self.user).aggregate(average=Avg('rating'))
        avg = 0
        if ratings ["average"] is not None:
            avg = float(ratings["average"])
        return avg

    def countrating(self):
        return UserRating.objects.filter(user_received=self.user).count()


	
	


#User Rating



class UserRating(models.Model):
    user_rated=models.ForeignKey(User,  related_name='given_ratings', on_delete=models.CASCADE)
    user_received=models.ForeignKey(User, related_name='received_ratings', on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )
   
    class Meta:
        verbose_name_plural='Ratings'
        constraints = [models.UniqueConstraint(fields=['user_rated', 'user_received'], name='one_rating_per_user')]

    def __str__(self):
        return f'{self.user_rated.username} gave {self.rating} to {self.user_received.username}' 


# messaging between users

class Message(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
	recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
	body = models.TextField(max_length=1000, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	is_read = models.BooleanField(default=False)

	def send_message(from_user, to_user, body):
		sender_message = Message(
			user=from_user,
			sender=from_user,
			recipient=to_user,
			body=body,
			is_read=True)
		sender_message.save()

		recipient_message = Message(
			user=to_user,
			sender=from_user,
			body=body,
			recipient=from_user,)
		recipient_message.save()
		return sender_message

	def get_messages(user):
		messages = Message.objects.filter(user=user).values('recipient').annotate(last=Max('date')).order_by('-last')
		users = []
		for message in messages:
			users.append({
				'user': User.objects.get(pk=message['recipient']),
				'last': message['last'],
				'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
				})
		return users