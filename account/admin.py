from django.contrib import admin
from .models import Profile, UserRating, Chat, Message

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'userbirth', 'phone_number', 'region', 'city', 'photo']


admin.site.register(Profile, ProfileAdmin)


class UserRatingAdmin(admin.ModelAdmin):
    list_display =('user_rated','user_received','rating' )
admin.site.register(UserRating,UserRatingAdmin)

class ChatAdmin(admin.ModelAdmin):
    list_display =('id','type' )
admin.site.register(Chat,ChatAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display =('chat','author', 'message' )
admin.site.register(Message,MessageAdmin)