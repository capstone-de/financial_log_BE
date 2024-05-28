from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Income, Expense, WithWhom
from user_app.models import User, Follow
from .serializers import IncomeSerializer, ExpenseSerializer, WithWhomSerializer

@csrf_exempt
@api_view(['POST'])
def saveIncome(request) :
    serializer = IncomeSerializer(data=request.data)
    if serializer.is_valid() :
        serializer.save()
        return JsonResponse({"message" : "success"}, status=200)
    else :
        return JsonResponse({"error" : serializer.errors}, status=400)

@api_view(['GET', 'POST'])
def saveExpense(request) :
    if request.method == 'GET':
        user = request.GET.get('user')
        following_id= Follow.objects.filter(follower = user, status = 1).values_list('following', flat=True)
        following_nickname = []
        for f_id in following_id:
            nickname = User.objects.get(user_id = f_id).nickname
            following_nickname.append(nickname)
        return Response(following_nickname)
    if request.method == 'POST':
        print(request.data)
        expenseSerializer = ExpenseSerializer(data=request.data)
        if expenseSerializer.is_valid() :
            inputExpense = expenseSerializer.data
            withwhomList = request.data.get('with_whom', [])
            expense = Expense(user=User.objects.get(user_id = inputExpense['user']), date=inputExpense['date'], price=inputExpense['price'], category=inputExpense['category'], bname=inputExpense['bname'], satisfaction=inputExpense['satisfaction'])
            expense.save()
            for withwhomItem in withwhomList :
                withwhom = withwhomItem.get('nickname')
                user_id = User.objects.get(nickname=withwhom).user_id
                withwhom = WithWhom(expense=expense, user=User.objects.get(user_id = user_id))
                withwhom.save()
            return JsonResponse({"message" : "success"}, status=200)
        else :
            return JsonResponse({"error" : serializers.errors}, status=403)