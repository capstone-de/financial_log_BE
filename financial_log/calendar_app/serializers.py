from rest_framework import serializers
from .models import Income, Expense, Diary

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ('category', 'price')

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('category', 'bname', 'price')

class DiaryCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ('date',)

class ExpenseCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('date',)

class IncomeCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ('date',)