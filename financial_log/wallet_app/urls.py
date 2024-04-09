from django.urls import path
from . import views

app_name = 'wallet_app'

urlpatterns = [
    path('saveIncome', views.saveIncome),
    path('saveExpense', views.saveExpense),
]