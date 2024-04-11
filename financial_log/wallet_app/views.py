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
        return JsonResponse({"error" : serializer.errors()}, status=400)

@api_view(['POST'])
def saveExpense(request) : 
    expenseSerializer = ExpenseSerializer(data=request.data)
    if expenseSerializer.is_valid() :
        inputExpense = expenseSerializer.data
        withwhomList = request.data.get('with_whom', [])
        for withwhomItem in withwhomList :
            try:
                nickname = User.objects.get(nickname=withwhomItem['nickname'])
            except User.DoesNotExist:
                return JsonResponse({"error" : "해당 닉네임을 가진 사용자가 존재하지 않습니다."}, status=403)

        expense = Expense(user=User.objects.get(user_id = inputExpense['user']), date=inputExpense['date'], price=inputExpense['price'], category=inputExpense['category'], bname=inputExpense['bname'], satisfaction=inputExpense['satisfaction'])
        expense.save()
        for withwhomItem in withwhomList :
            user_id = User.objects.get(nickname = withwhomItem['nickname']).user_id
            withwhom = WithWhom(expense=expense, user=User.objects.get(user_id = user_id))
            withwhom.save()
        return JsonResponse({"message" : "success"}, status=200)
    else :
        return JsonResponse({"error" : serializer.errors}, status=403)