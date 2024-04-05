from django.db import models

from user_app.models import User

class Income(models.Model):
    income_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    category = models.CharField(max_length=16)
    date = models.DateTimeField()
    memo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Income'


class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    category = models.CharField(max_length=36)
    bname = models.CharField(max_length=20)
    date = models.DateTimeField()
    satisfaction = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Expense'

class Withwhom(models.Model):
    table_id = models.AutoField(primary_key=True)
    expense_id = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'WithWhom'