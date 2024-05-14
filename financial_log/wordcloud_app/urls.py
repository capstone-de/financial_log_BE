from django.urls import path
from . import views

app_name = 'wordcloud_app'

urlpatterns = [
    path('myDiary', views.myDiary),
    path('diary', views.diary),
]