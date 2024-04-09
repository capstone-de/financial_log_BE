from django.urls import path
from . import views

app_name = 'diary_app'

urlpatterns = [
    path('diaryList', views.diaryList),
    path('myDiaryList', views.myDiaryList),
    path('saveDiary', views.saveDiary),
]