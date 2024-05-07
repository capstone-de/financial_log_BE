from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user_app.models import User
from wallet_app.models import Income, Expense
from .serializers import *

from django.db.models import Sum, Avg
from datetime import datetime, timedelta

@csrf_exempt
@api_view(['GET'])
def daily(request):
    user = request.GET.get('user')
    date = request.GET.get('date')

    incomes = Income.objects.filter(user = User.objects.get(user_id = user), date = date).values('price')
    expenses = Expense.objects.filter(user = User.objects.get(user_id = user), date = date).values('category', 'bname', 'price')
    total_incomes = incomes.aggregate(total=Sum('price'))['total']
    total_expenses = expenses.aggregate(total=Sum('price'))['total']
    daily = {
        'total_income' : total_incomes,
        'total_expenses' : total_expenses,
        'expenses' : expenses
    }
    return Response(daily)

@api_view(['GET'])
def weekly(request):
    user = request.GET.get('user')
    date = datetime.strptime(request.GET.get('date'), '%Y-%m-%d').date()
    
    week_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    weekly = {}
    
    for i in range(7):
        incomes = Income.objects.filter(user = User.objects.get(user_id = user), date = date + timedelta(days=i)).values('category', 'price')
        expenses = Expense.objects.filter(user = User.objects.get(user_id = user), date = date + timedelta(days=i)).values('category', 'price')
        total_incomes = incomes.aggregate(total=Sum('price'))['total']
        total_expenses = expenses.aggregate(total=Sum('price'))['total']
        weekly[week_list[i]] = {
            "total_income": total_incomes,
            "total_expense": total_expenses
        }
    category_income = Income.objects.filter(user = User.objects.get(user_id = user), date__range=[date, date+timedelta(days=6)]).values('category').annotate(total_income=Sum('price'))
    category_expense = Expense.objects.filter(user = User.objects.get(user_id = user), date__range=[date, date+timedelta(days=6)]).values('category').annotate(total_expense=Sum('price'))
    weekly['category'] = {
        "income": list(category_income),
        "expense": list(category_expense)
    }
    return Response(weekly)

@api_view(['GET'])
def monthly(request):
    user = request.GET.get('user')
    year = request.GET.get('year')
    month = int(request.GET.get('month'))

    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly = {}
    null=[]

    for i in range(4):
        expenses = Expense.objects.filter(user = User.objects.get(user_id = user), date__year = year, date__month = month - i).values('category', 'price', 'satisfaction')
        incomes = Income.objects.filter(user = User.objects.get(user_id = user), date__year = year, date__month = month - i).values('category', 'price')
        total_incomes = incomes.aggregate(total=Sum('price'))['total']
        total_expenses = expenses.aggregate(total=Sum('price'))['total']
        monthly[month_list[month - i - 1]] = {
            "total_income": total_incomes,
            "total_expense": total_expenses
        }
    
    last_category_expense = Expense.objects.filter(user = User.objects.get(user_id = user), date__year = year, date__month = month - 1).values('category').annotate(total_expense=Sum('price'))
    this_category_expense = Expense.objects.filter(user = User.objects.get(user_id = user), date__year = year, date__month = month).values('category').annotate(total_expense=Sum('price'))
    monthly['category'] = {
        "last_month": list(last_category_expense),
        "this_month": list(this_category_expense)
    }
    satisfaction_expense = Expense.objects.filter(user = User.objects.get(user_id = user), date__year = year, date__month = month).values('category', 'bname', 'price', 'satisfaction').order_by('-satisfaction').first()
    monthly['satisfaction'] = {
        "satisfaction": satisfaction_expense
    }
    return Response(monthly)


@api_view(['GET'])
def yearly(request):
    user = request.GET.get('user')
    year = request.GET.get('year')

    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    yearly = {}

    for i in range(12):
        incomes = Income.objects.filter(user = User.objects.get(user_id = user), date__year = year, date__month = i+1).aggregate(total=Sum('price'))['total']
        expenses = Expense.objects.filter(user = User.objects.get(user_id = user), date__year = year, date__month = i+1).aggregate(total=Sum('price'))['total']
        yearly[month_list[i]] = {
            "total_income": incomes,
            "total_expense": expenses
        }
    category_expense = Expense.objects.filter(user = User.objects.get(user_id = user), date__year = year).values('category').annotate(total_expense=Sum('price'))
    yearly['category'] = {
        "yearly": list(category_expense)
    }
    satisfaction = Expense.objects.filter(user = User.objects.get(user_id = user), date__year = year).values('category').annotate(average_satisfaction=Avg('satisfaction'))
    yearly['satisfaction'] = {
        "yearly": list(satisfaction)
    }
    return Response(yearly)