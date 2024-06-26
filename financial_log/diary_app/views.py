from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Diary, Image, Hashtag, DiaryHashtag
from wallet_app.models import Expense
from user_app.models import User, Follow

from .serializers import DiarySerializer, ImageSerializer
from wallet_app.serializers import DiaryExpenseSerializer

from django.conf import settings
import base64

# Create your views here.
@csrf_exempt
@api_view(['GET'])
def diaryList(request):
    if request.method == 'GET' : 
        user = request.GET.get('user')

        followList = Follow.objects.filter(following=user, status = 1)
        followerList = []
        for follower in followList:
            followerList.append(User.objects.get(user_id = follower.follower.user_id).user_id)
        diaryList = Diary.objects.filter(privacy = 1, user__in=followerList).order_by('-date')[:10]
        diaryListResult = []
        for diary in diaryList:
            hashtagList = DiaryHashtag.objects.filter(diary = diary.diary_id)
            imageList = Image.objects.filter(diary = diary.diary_id)
            return_hashtag = []
            return_images = []
            for hashtagItem in hashtagList:
                hashtag = Hashtag.objects.get(hashtag = hashtagItem.hashtag.hashtag).hashtag
                return_hashtag.append(hashtag)
            for imageItem in imageList:
                image_path = '_media/' + imageItem.image.decode('utf-8')
                try:
                    with open(image_path, 'rb') as image_file:
                        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                        # Base64 인코딩된 이미지 데이터를 리스트에 추가
                        return_images.append(encoded_image)
                except Exception as e:
                    print(f"Error encoding image: {e}")
            diaryData = {
                'nickname': User.objects.get(user_id = diary.user.user_id).nickname,
                'date': diary.date,
                'contents': diary.contents,
                'hashtag': return_hashtag,
                'image' : return_images
            }
            diaryListResult.append(diaryData)
        return Response(diaryListResult)
    return JsonResponse({"message" : "fail"}, status = 403)

@csrf_exempt
@api_view(['GET'])
def myDiaryList(request): 
    user = request.GET.get('user')
    nickname = User.objects.get(user_id = user).nickname
    follower = Follow.objects.filter(follower=user, status = 1).count()
    following = Follow.objects.filter(following=user, status = 1).count()

    myDiaryList = Diary.objects.filter(user_id = user).order_by('-date')[:10]
    myDiaryListResult = []
    for myDiary in myDiaryList:
        hashtagList = DiaryHashtag.objects.filter(diary = myDiary.diary_id)
        imageList = Image.objects.filter(diary = myDiary.diary_id)
        return_hashtag = []
        return_images = []
        for hashtagItem in hashtagList:
            hashtag = Hashtag.objects.get(hashtag = hashtagItem.hashtag.hashtag).hashtag
            return_hashtag.append(hashtag)
        for imageItem in imageList:
                image_path = '_media/' + imageItem.image.decode('utf-8')
                try:
                    with open(image_path, 'rb') as image_file:
                        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                        # Base64 인코딩된 이미지 데이터를 리스트에 추가
                        return_images.append(encoded_image)
                except Exception as e:
                    print(f"Error encoding image: {e}")
        diary_data = {
            'date': myDiary.date,
            'contents': myDiary.contents,
            'hashtag': return_hashtag,
            'image' : return_images
        }
        myDiaryListResult.append(diary_data)

    myDiaryListData = {
        "nickname" : nickname,
        "follower" : follower,
        "following" : following,
        "myDiaryList" : myDiaryListResult
    }
    return Response(myDiaryListData)

@csrf_exempt
@api_view(['GET', 'POST'])
def saveDiary(request):
    if request.method == 'GET' : 
        user = request.GET.get('user')
        date = request.GET.get('date')
        if Diary.objects.filter(user=user, date = date) :
            print("일기 이미 작성함")
            return JsonResponse({"message" : "이미 일기를 작성했습니다."}, status=403)
        expenses = Expense.objects.filter(user=user, date=date)
        diaryExpenseSerializer = DiaryExpenseSerializer(expenses, many=True)
        print(diaryExpenseSerializer.data)
        return Response(diaryExpenseSerializer.data)
    
    if request.method == 'POST' : 
        diarySerializer = DiarySerializer(data = request.data)
        imageList = request.FILES.getlist('image')
        print(request.data)
        print(imageList)
        if diarySerializer.is_valid() :
            data = diarySerializer.data
            hashtagList = request.data.get('hashtag', [])
            diary = Diary(user=User.objects.get(user_id = data['user']), date=data['date'], contents=data['contents'], privacy=data['privacy'])
            diary.save()
            for imageListItem in imageList :
                image = Image(diary = diary, image = imageListItem)
                image.save()
            for hashtagListItem in hashtagList :
                if not Hashtag.objects.filter(hashtag=hashtagListItem):
                    hashtag = Hashtag(hashtag = hashtagListItem)
                    hashtag.save()
                diaryHashtag = DiaryHashtag(diary = diary, hashtag = Hashtag.objects.get(hashtag=hashtagListItem))
                diaryHashtag.save()
            return JsonResponse({"message" : "success"}, status=200)
        else :
            return JsonResponse({"error": diarySerializer.errors}, status=403)
