from rest_framework import serializers
from .models import Income, Expense, WithWhom

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ('user', 'date', 'price', 'category', 'memo')

class WithWhomSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithWhom
        fields = ('user',)

class ExpenseSerializer(serializers.ModelSerializer):
    with_whom = WithWhomSerializer(many=True, read_only=True)
    class Meta:
        model = Expense
        fields = ('user', 'date', 'price', 'category', 'bname', 'with_whom', 'satisfaction')

class DiaryExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('category', 'bname', 'price')
