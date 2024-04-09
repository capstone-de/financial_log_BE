from rest_framework import serializers
from .models import Diary, Image, Hashtag

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        field = ('hashtag',)

class DiarySerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(many=True, read_only=True)
    class Meta:
        model = Diary
        fields = ('user', 'date', 'contents', 'hashtag', 'privacy')

class MyDiarySerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(many=True, read_only=True)
    class Meta:
        model = Diary
        fields = ('user', 'date', 'contents', 'hashtag', 'privacy')
