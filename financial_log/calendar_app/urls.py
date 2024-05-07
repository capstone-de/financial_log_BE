from django.urls import path
from . import views

app_name = 'calendar_app'

urlpatterns = [
    path('getWalletIncome', views.getWalletIncome),
    path('getWalletExpense', views.getWalletExpense),
    path('getCalendar', views.getCalendar),
]