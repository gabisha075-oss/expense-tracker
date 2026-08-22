from django.contrib import admin
from .models import Category, Income, Expense, Budget, BudgetAlert, MoneySavingQuote

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'emoji', 'user')
    list_filter = ('category_type', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'date', 'created_at')
    list_filter = ('date', 'category', 'user')
    search_fields = ('description', 'user__username')
    readonly_fields = ('created_at',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'payment_method', 'date', 'created_at')
    list_filter = ('date', 'category', 'payment_method', 'user')
    search_fields = ('description', 'user__username')
    readonly_fields = ('created_at',)

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'frequency', 'alert_threshold')
    list_filter = ('frequency', 'user')
    search_fields = ('category__name', 'user__username')

@admin.register(BudgetAlert)
class BudgetAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'budget', 'status', 'spent_amount', 'created_at', 'is_read')
    list_filter = ('status', 'is_read', 'created_at')
    search_fields = ('user__username', 'budget__category__name')
    readonly_fields = ('created_at',)

@admin.register(MoneySavingQuote)
class MoneySavingQuoteAdmin(admin.ModelAdmin):
    list_display = ('quote', 'author', 'emoji')
    search_fields = ('quote', 'author')
