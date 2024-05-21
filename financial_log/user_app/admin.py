from django.contrib import admin
from .models import User, Follow

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'nickname']

class FollowAdmin(admin.ModelAdmin):
    list_display = ['follow_id', 'follower', 'following', 'status']

admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)