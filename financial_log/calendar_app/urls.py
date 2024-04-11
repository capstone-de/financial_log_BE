from django.urls import path
from . import views

app_name = 'calendar_app'

urlpatterns = [
    path('getWallet', views.getWallet),
    path('getCalendar', views.getCalendar),
]