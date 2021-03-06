from django.contrib import admin
from .models import Profile, UserRating, Message

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'userbirth', 'phone_number', 'region', 'city', 'photo']


admin.site.register(Profile, ProfileAdmin)


class UserRatingAdmin(admin.ModelAdmin):
    list_display =('user_rated','user_received','rating' )
admin.site.register(UserRating,UserRatingAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'sender', 'recipient', 'body')

admin.site.register(Message, MessageAdmin)

