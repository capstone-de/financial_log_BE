from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Income, Expense, WithWhom
from user_app.models import User
from .serializers import IncomeSerializer, ExpenseSerializer, WithWhomSerializer

# Create your views here.
@csrf_exempt
@api_view(['POST'])
def saveIncome(request) : 
    serializer = IncomeSerializer(data=request.data)
    if serializer.is_valid() :
        serializer.save()
        return JsonResponse({"message" : "success"}, status=200)
    else :
        return JsonResponse({"message" : "fail"}, status=400)

@api_view(['POST'])
def saveExpense(request) : 
    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid() :
        data = serializer.data
        withwhom_data = request.data.get('with_whom', [])
        expense = Expense(user=User.objects.get(user_id = data['user']), date=data['date'], price=data['price'], category=data['category'], bname=data['bname'], satisfaction=data['satisfaction'])
        expense.save()
        for item in withwhom_data :
            user_id = item['user']
            withwhom = WithWhom(expense=expense, user=User.objects.get(user_id = user_id))
            withwhom.save()
        return JsonResponse({"message" : "success"}, status=200)
    else :
        return JsonResponse({"message" : "fail"}, status=400)



