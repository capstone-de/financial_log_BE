from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Expense, Income, Diary
from .serializers import ExpenseSerializer, IncomeSerializer
from .serializers import DiaryCalendarSerializer, ExpenseCalendarSerializer, IncomeCalendarSerializer

# @api_view(['GET'])
# def getWallet(request):
#     user = request.GET.get('user')
#     date = request.GET.get('date')
#     try:
#         user_id = User.objects.get(user_id=user)
#     except User.DoesNotExist:
#         return Response({"error": "User not found"}, status=404)
#     incomes = Income.objects.filter(user = User.objects.get(user_id = user), date = date)
#     incomeSerializer = IncomeSerializer(incomes, many=True)
#     expenses = Expense.objects.filter(user = User.objects.get(user_id = user), date = date)
#     expenseSerializer = ExpenseSerializer(expenses, many=True)
#     walletData = {
#         "income": incomeSerializer.data,
#         "expense": expenseSerializer.data
#     }
#     print(walletData)
#     return Response(walletData)

@api_view(['GET'])
def getWalletIncome(request):
    user = request.GET.get('user')
    date = request.GET.get('date')
    try:
        user_id = User.objects.get(user_id=user)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    incomes = Income.objects.filter(user = User.objects.get(user_id = user), date = date)
    incomeSerializer = IncomeSerializer(incomes, many=True)
    walletData = {
        "income": incomeSerializer.data
    }
    print(walletData)
    return Response(walletData)

@api_view(['GET'])
def getWalletExpense(request):
    user = request.GET.get('user')
    date = request.GET.get('date')
    try:
        user_id = User.objects.get(user_id=user)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    expenses = Expense.objects.filter(user = User.objects.get(user_id = user), date = date)
    expenseSerializer = ExpenseSerializer(expenses, many=True)
    walletData = {
        "expense": expenseSerializer.data
    }
    print(walletData)
    return Response(walletData)

@api_view(['GET'])
def getCalendar(request):
    user = request.GET.get('user')
    year = request.GET.get('year')
    month = request.GET.get('month')
    try:
        user_id = User.objects.get(user_id=user)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    diaries = Diary.objects.filter(user=User.objects.get(user_id = user), date__year = year, date__month = month).values('date').order_by('date').distinct()
    expenses = Expense.objects.filter(user = User.objects.get(user_id = user), date__year = year, date__month = month).values('date').order_by('date').distinct()
    incomes = Income.objects.filter(user = User.objects.get(user_id = user), date__year = year, date__month = month).values('date').order_by('date').distinct()
    diarySerializer = DiaryCalendarSerializer(diaries, many = True)
    expenseSerializer = ExpenseCalendarSerializer(expenses, many=True)
    incomeSerializer = IncomeCalendarSerializer(incomes, many=True)
    date_list = [item["date"] for item in diarySerializer.data]
    expense_list = [item["date"] for item in expenseSerializer.data]
    income_list = [item["date"] for item in incomeSerializer.data]
    getCalendarData = {
        "diary": date_list,
        "expense" : expense_list,
        "income" : income_list
    }
    print(getCalendarData)
    return Response(getCalendarData)