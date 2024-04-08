from django.contrib import admin
from .models import Diary, Image, Hashtag, DiaryHashtag

# Register your models here.
admin.site.register(Diary)
admin.site.register(Image)
admin.site.register(Hashtag)
admin.site.register(DiaryHashtag)