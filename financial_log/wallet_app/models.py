from django.db import models

from user_app.models import User
from user_app.models import Follow

class Income(models.Model):
    income_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.IntegerField()
    category = models.CharField(max_length=16)
    memo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Income'


class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    category = models.CharField(max_length=36)
    bname = models.CharField(max_length=20)
    date = models.DateField()
    satisfaction = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Expense'

class WithWhom(models.Model):
    table_id = models.AutoField(primary_key=True)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'WithWhom'