from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user_app.models import User
from wallet_app.models import Income, Expense
from diary_app.models import Diary, Hashtag, DiaryHashtag, Gu

from django.db.models import Sum, Avg
from datetime import datetime, timedelta

from transformers import pipeline
from scipy.stats import pearsonr

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


# 감성 분석 모델 로드
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# 감성 분석 함수
def analyze_sentiment(text):
    try:
        result = sentiment_pipeline(text[:500])
        if result[0]['label'] in ['5 stars', '4 stars', '3 stars']:
            return {'label': 'POSITIVE', 'score': result[0]['score']}
        else:
            return {'label': 'NEGATIVE', 'score': result[0]['score']}
    except Exception as e:
        print(f"감성 분석 중 오류 발생: {e}")
        return None

@api_view(['GET'])
def sentimentAnalysis(request):
    user = request.GET.get('user')
    year = request.GET.get('year')
    month = request.GET.get('month')

    # 일기와 지출 데이터를 모두 갖고 있는 날짜 필터링
    diary_dates = Diary.objects.filter(user=User.objects.get(user_id=user), date__year=year, date__month=month).values_list('date', flat=True)
    expense_dates = Expense.objects.filter(user=User.objects.get(user_id=user), date__year=year, date__month=month).values_list('date', flat=True)

    # 일기와 지출이 모두 있는 날짜만 선택
    common_dates = set(diary_dates).intersection(set(expense_dates))

    if not common_dates : 
        result = {
            'coordinate': [],  
            'correlation': 0  
        }
        return Response(result)

    # 공통 날짜에 해당하는 일기와 지출 데이터 가져오기
    diaries = Diary.objects.filter(user=User.objects.get(user_id=user), date__in=common_dates).values('date', 'contents')
    expenses = Expense.objects.filter(user=User.objects.get(user_id=user), date__in=common_dates).values('date', 'price')

    sentiment_results = []
    expenditure_values = []
    coordinates = []

    # 각 일기의 내용에 대해 감성 분석 수행 및 결과 저장
    for diary in diaries:
        sentiment_result = analyze_sentiment(diary['contents'])
        if sentiment_result:
            score = 0  # 기본 점수는 0으로 설정
            if sentiment_result['label'] == 'POSITIVE':
                score = round(sentiment_result['score'] - 3, 2) # 긍정 점수를 그대로 사용
            elif sentiment_result['label'] == 'NEGATIVE':
                score = round(-sentiment_result['score'], 2)  # 부정 점수는 음수로 변환하여 사용
            
            # 해당 일기의 날짜에 맞는 지출 금액 찾기
            expenditure = next((expense['price'] for expense in expenses if expense['date'] == diary['date']), 0)
            
            sentiment_results.append(score)
            expenditure_values.append(expenditure)
            coordinates.append((score, expenditure))  # (감정 점수, 지출 금액) 형태로 저장

    print("sentiment_results" + str(sentiment_results))
    print("expenditure_values" + str(expenditure_values))

    # 피어슨 상관계수 계산
    correlation = 0
    if len(sentiment_results) >= 1 and len(expenditure_values) >= 1:
        correlation, _ = pearsonr(sentiment_results, expenditure_values)

    result = {
        'coordinate': coordinates,  # (감정분석수행 결과, 금액) 리스트
        'correlation': round(correlation,2)
    }

    return Response(result)

@api_view(['GET'])
def locationAnalysis(request):
    user = request.GET.get('user')
    year = request.GET.get('year')
    month = request.GET.get('month')

    # 일기와 지출 데이터를 모두 갖고 있는 날짜 필터링
    diary_dates = Diary.objects.filter(user=User.objects.get(user_id=user), date__year=year, date__month=month).values_list('date', flat=True)
    expense_dates = Expense.objects.filter(user=User.objects.get(user_id=user), date__year=year, date__month=month).values_list('date', flat=True)

    # 일기와 지출이 모두 있는 날짜만 선택
    common_dates = set(diary_dates).intersection(set(expense_dates))

    if not common_dates :
        result = {
            'gu': "",
            'total_expenditure' : 0
        }
        return Response(result)

    # 일기와 지출 데이터를 미리 가져오기
    diaries = Diary.objects.filter(user=User.objects.get(user_id=user), date__in=common_dates).values('date', 'gu')
    expenses_dict = {expense['date']: expense['price'] for expense in Expense.objects.filter(user=User.objects.get(user_id=user), date__in=common_dates).values('date', 'price')}

    result = []

    # 구 정보를 미리 가져와서 저장
    gu_names = {gu_obj.gu_id: gu_obj.gu for gu_obj in Gu.objects.all()}

    for gu in range(1, 26):
        total_expenditure = 0
        for diary in diaries:
            if diary['gu'] == gu:
                total_expenditure += expenses_dict.get(diary['date'], 0)
        result.append({'gu': gu_names.get(gu, ''), 'total_expenditure': total_expenditure})

    return Response(result)