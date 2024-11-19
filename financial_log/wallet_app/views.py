from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Income, Expense, WithWhom
from user_app.models import User, Follow
from .serializers import IncomeSerializer, ExpenseSerializer, WithWhomSerializer

from django.conf import settings

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


from django.conf import settings

def reverse_lines(text):
    lines = text.splitlines()
    reversed_lines = lines[::-1]
    reversed_text = '\n'.join(reversed_lines)
    return reversed_text

# 총 지불 금액 추출 함수
def extract_total_amount(text):
    reversed_text = reverse_lines(text)
    # '합계' 뒤에 나오는 금액을 우선적으로 찾고 없으면 다른 금액을 탐색
    total_amount_pattern = re.search(r'(합\s?계|총합계|[Tt]otal)\s*[:\s]?\s*([\d,]+)\s*원?', reversed_text)
    if total_amount_pattern:
        total_amount = total_amount_pattern.group(2)
        return total_amount.replace(",", "") 
    # '합계'가 없으면 다른 금액 관련 키워드로 검색
    amount_pattern = re.search(r'(판매총액|받을금액|금\s?액|총액|신용액|결제금액|신용카드|받은돈|total|Total)\s*[:\s]?\s*([\d,]+)\s*원?', reversed_text)
    # 금액 추출
    if amount_pattern:
        amount = amount_pattern.group(2)
        return amount.replace(",", "")  
    else:
        return "총 지불 금액을 찾을 수 없습니다."

@csrf_exempt
@api_view(['POST'])
def saveExpenseOCR(request) :
    user = request.GET.get('user')
    date = request.GET.get('date')
    image = request.FILES.get('image')

    files = [('file', image)]

    request_json = {'images' : [{'format' : 'jpeg', 'name' : 'demo'}],
                'requestId' : str(uuid.uuid4()),
                'version' : 'V2',
                'timestamp' : int(round(time.time() * 1000))
                }
    payload = {'message' : json.dumps(request_json).encode('UTF-8')}
    headers = {'X-OCR-SECRET' : settings.SECRET_KEY}

    response = requests.request("POST", settings.APIGY_URL, headers = headers, data = payload, files = files)
    result = response.json()

    string_result = ''
    for i in result['images'][0]['fields']:
        if i['lineBreak'] == True:
            linebreak = '\n'
        else:
            linebreak = ' '
        string_result = string_result + i['inferText'] + linebreak

    print(string_result)

    amount = extract_total_amount(string_result)
    print("금액:", amount)

    if amount == "총 지불 금액을 찾을 수 없습니다.":
        return JsonResponse({"message" : "fail"}, status = 403)
    else : 
        response = {
            'amount': amount
            }
        return Response(response)





