from rest_framework import serializers
from .models import Diary, Image, Hashtag

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('hashtag',)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', )

class DiarySerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(many=True, read_only=True)
    image = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = Diary
        fields = ('user', 'date', 'contents', 'privacy', 'hashtag', 'location')