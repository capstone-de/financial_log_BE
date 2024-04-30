from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user_app.models import User
from wallet_app.models import Income, Expense
from .serializers import *

# Create your views here.
@csrf_exempt
@api_view(['GET'])
def daily(request):
    user = request.GET.get('user')
    date = request.GET.get('date')

    expenses = Expense.objects.filter(user = User.objects.get(user_id = user), date = date)
    incomes = Income.objects.filter(user = User.objects.get(user_id = user), date = date)
    expenseSerializer = DailyExpenseSerializer(expenses, many=True)
    incomeSerializer = DailyIncomeSerializer(incomes, many=True)
    daily = {
        "expense": expenseSerializer.data,
        "income": incomeSerializer.data
    }
    return Response(daily)

@api_view(['GET'])
def weekly(request):
    user = request.GET.get('user')
    date = request.GET.get('date')