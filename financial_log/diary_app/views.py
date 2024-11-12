from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Diary, Image, Hashtag, DiaryHashtag, Gu
from wallet_app.models import Expense
from user_app.models import User, Follow

from .serializers import DiarySerializer, ImageSerializer
from wallet_app.serializers import DiaryExpenseSerializer

from django.conf import settings
import boto3
from uuid import uuid4
from django.conf import settings

# Create your views here.

# S3에 파일을 업로드
def upload_image_to_s3(image_file, user_id):
    try : 
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        # 이미지 파일에 고유한 이름을 생성
        image_key = f"diary_images/{user_id}/{uuid4()}/{image_file.name}"
        # S3에 이미지 업로드
        s3.upload_fileobj(
            image_file,
            settings.AWS_STORAGE_BUCKET_NAME,
            image_key,
            ExtraArgs={"ContentType": image_file.content_type}
        )
        # S3에 저장된 이미지의 URL 반환
        image_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{image_key}"
        return image_url
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None

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
            
            return_images = [imageItem.image for imageItem in imageList]
            for hashtagItem in hashtagList:
                hashtag = Hashtag.objects.get(hashtag = hashtagItem.hashtag.hashtag).hashtag
                return_hashtag.append(hashtag)
           
            diaryData = {
                'nickname': User.objects.get(user_id = diary.user.user_id).nickname,
                'date': diary.date,
                'contents': diary.contents,
                'hashtag': return_hashtag,
                'image' : return_images,
                'gu': Gu.objects.get(gu_id = diary.gu_id).gu
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
        # 이미지 URL을 그대로 반환
        return_images = [imageItem.image for imageItem in imageList]
        for hashtagItem in hashtagList:
            hashtag = Hashtag.objects.get(hashtag = hashtagItem.hashtag.hashtag).hashtag
            return_hashtag.append(hashtag)
        
        diary_data = {
            'date': myDiary.date,
            'contents': myDiary.contents,
            'hashtag': return_hashtag,
            'image' : return_images,
            'gu': Gu.objects.get(gu_id = diary.gu_id).gu
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
            # 이미지 파일 유무에 따라 해시태그 가져오기
            if imageList:
                hashtagList = request.data.getlist('hashtag')  # 이미지가 있는 경우
            else:
                hashtagList = request.data.get('hashtag', [])  # 이미지가 없는 경우
            
            gu = Gu.objects.get(gu=request.data.get('gu'))
            diary = Diary(user=User.objects.get(user_id = data['user']), date=data['date'], contents=data['contents'], privacy=data['privacy'], gu = gu)
            diary.save()

            for imageListItem in imageList :
                image_url = upload_image_to_s3(imageListItem, data['user'])
                image = Image(diary=diary, image=image_url)  # S3 URL을 저장
                print(image)
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