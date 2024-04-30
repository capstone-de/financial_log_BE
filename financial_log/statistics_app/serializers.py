from rest_framework import serializers
from .models import Income, Expense, User

class DailyIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ('category', 'price')

class DailyExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('category', 'price')