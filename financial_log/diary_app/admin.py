from django.contrib import admin
from .models import Diary, Image, Hashtag, DiaryHashtag, User

# Register your models here.

class DiaryAdmin(admin.ModelAdmin):
    list_display = ['diary_id', 'user','date', 'contents', 'privacy']
    
    
class HashtagAdmin(admin.ModelAdmin):
    list_display = ['hashtag_id', 'hashtag']
    
class DiaryHashtagAdmin(admin.ModelAdmin):
    list_display = ['table_id', 'diary','hashtag']
    
admin.site.register(Diary, DiaryAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(DiaryHashtag, DiaryHashtagAdmin)
admin.site.register(Image)