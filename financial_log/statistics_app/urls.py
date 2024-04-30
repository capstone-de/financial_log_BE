from django.urls import path
from . import views

app_name = 'statistics_app'

urlpatterns = [
    path('daily', views.daily),
    path('weekly', views.weekly),
    path('monthly', views.monthly),
     path('yearly', views.yearly),
]