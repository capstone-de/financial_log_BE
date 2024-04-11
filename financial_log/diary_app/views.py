from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Diary, Image, Hashtag, DiaryHashtag
from wallet_app.models import Expense
from user_app.models import User, Follow
from .serializers import DiarySerializer, MyDiarySerializer
from wallet_app.serializers import DiaryExpenseSerializer

# Create your views here.
@csrf_exempt
@api_view(['GET'])
def diaryList(request) :
    if request.method == 'GET' : 
        diaryList = Diary.objects.filter(privacy = 1).order_by('diary_id')[:10]
        serializer = DiarySerializer(diaryList, many=True)
        return Response(serializer.data)
    return JsonResponse({"message" : "fail"}, status = 403)

@csrf_exempt
@api_view(['GET'])
def myDiaryList(request) : 
    if request.method == 'GET' : 
        user = request.GET.get('user')
        follower = Follow.objects.filter(follower=User.objects.get(user_id = user), status = 1).count()
        following = Follow.objects.filter(following=User.objects.get(user_id = user), status = 1).count()
        myDiaryList = Diary.objects.filter(user_id = User.objects.get(user_id = user)).order_by('diary_id')[:10]
        serializer = MyDiarySerializer(myDiaryList, many=True)
        data = {
            "follower" : follower,
            "following" : following,
            "myDiaryList" : serializer.data
        }
        return Response(data)
    return JsonResponse({"message" : "fail"}, status = 403)

@csrf_exempt
@api_view(['GET', 'POST'])
def saveDiary(request) :
    if request.method == 'GET' : 
        user = request.GET.get('user')
        date = request.GET.get('date')
        if Diary.objects.filter(user=User.objects.get(user_id = user), date = date) :
            return JsonResponse({"message" : "이미 일기를 작성했습니다."}, status=400)
        expenses = Expense.objects.filter(user=User.objects.get(user_id = user), date=date)
        serializer = DiaryExpenseSerializer(expenses, many=True)
        return Response(serializer.data)
    if request.method == 'POST' : 
        serializer = DiarySerializer(data = request.data)
        if serializer.is_valid() :
            data = serializer.data
            hashtag_data = request.data.get('hashtag', [])
            image_data = request.data.get('file', [])
            diary = Diary(user=User.objects.get(user_id = data['user']), date=data['date'], contents=data['contents'], privacy=data['privacy'])
            diary.save()
            for item in hashtag_data :
                if not Hashtag.objects.filter(hashtag=item):
                    hashtag = Hashtag(hashtag = item)
                    hashtag.save()
                diaryHashtag = DiaryHashtag(diary = diary, hashtag = Hashtag.objects.get(hashtag=item))
                diaryHashtag.save()
            return JsonResponse({"message" : "success"}, status=200)
        else :
            return JsonResponse({"message" : "fail"}, status=400)

                
                
            
    
    
