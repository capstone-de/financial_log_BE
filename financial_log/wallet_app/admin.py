from django.contrib import admin
from .models import Income, Expense, WithWhom

# Register your models here.

class ImcomeAdmin(admin.ModelAdmin):
    list_display = ['income_id', 'user', 'date', 'price', 'category', 'memo']

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['expense_id', 'user', 'date', 'price', 'category', 'bname', 'satisfaction']

class withWhomAdmin(admin.ModelAdmin):
    list_display = ['table_id', 'expense', 'user']

admin.site.register(Income, ImcomeAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(WithWhom, withWhomAdmin)