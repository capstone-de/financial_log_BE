from django.shortcuts import render
from django.http import JsonResponse
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *

from wordcloud import WordCloud
from collections import Counter
from itertools import cycle
import matplotlib.pyplot as plt

colors1 = cycle(["#4c8df7", "#e49995", "#fbe64d"])
colors2 = cycle(["#c6dcfc", "#f7e0df", "#fef8ba"])

def color_func1(word, font_size, position, orientation, random_state=None, **kwargs):
    return next(colors1)

def color_func2(word, font_size, position, orientation, random_state=None, **kwargs):
    return next(colors2)

# Create your views here.
@csrf_exempt
@api_view(['GET'])
def myDiary(request):
    user = request.GET.get('user')

    myDiary_list = Diary.objects.filter(user = user).values_list('diary_id', flat=True)
    myHashtag_list = []
    for diary_id in myDiary_list:
        temp_list = DiaryHashtag.objects.filter(diary = diary_id).values_list('hashtag', flat=True)
        myHashtag_list.extend(temp_list)
    myWord_list = []
    for hashtag_id in myHashtag_list:
        temp_list = Hashtag.objects.filter(hashtag_id = hashtag_id).values_list('hashtag', flat = True)
        myWord_list.extend(temp_list)
    # myWord_list = Hashtag.objects.filter(diaryhashtag__diary__user=user).values_list('hashtag', flat=True)

    word_count = Counter(myWord_list)

    wordcloud = WordCloud(width=300, height=300, 
                      background_color='white', 
                      color_func=color_func1,
                      min_font_size=10).generate_from_frequencies(word_count)

    image_path = "./wordcloud_app/media/myDiary.png"
    wordcloud.to_file(image_path)
    response = FileResponse(open(image_path, 'rb'), content_type='image/png')
    
    return response

@csrf_exempt
@api_view(['GET'])
def diary(request):
    diary_list = Diary.objects.filter(privacy = 1).values_list('diary_id', flat=True)
    hashtag_list = []
    for diary_id in diary_list:
        temp_list = DiaryHashtag.objects.filter(diary = diary_id).values_list('hashtag', flat=True)
        hashtag_list.extend(temp_list)
    word_list = []
    for hashtag_id in hashtag_list:
        temp_list = Hashtag.objects.filter(hashtag_id = hashtag_id).values_list('hashtag', flat = True)
        word_list.extend(temp_list)

    word_count = Counter(word_list)

    wordcloud = WordCloud(width=300, height=300, 
                      background_color='white', 
                      color_func=color_func2,
                      min_font_size=10).generate_from_frequencies(word_count)

    image_path = "./wordcloud_app/media/diary.png"
    wordcloud.to_file(image_path)
    response = FileResponse(open(image_path, 'rb'), content_type='image/png')
    
    return response