from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

class Category(models.Model):
    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    emoji = models.CharField(max_length=10, default='💰')
    color = models.CharField(max_length=7, default='#3498db')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ['user', 'name', 'category_type']


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, 
                                 limit_choices_to={'category_type': 'income'})
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - Income: {self.amount}"

    class Meta:
        ordering = ['-date']


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 limit_choices_to={'category_type': 'expense'})
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, default='Cash')
    date = models.DateField(default=timezone.now)
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - Expense: {self.amount}"

    class Meta:
        ordering = ['-date']


class Budget(models.Model):
    FREQUENCY_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                 limit_choices_to={'category_type': 'expense'})
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='monthly')
    month = models.IntegerField(default=1)  # 1-12 for monthly, 1 for yearly
    year = models.IntegerField(default=2026)
    alert_threshold = models.IntegerField(default=80)  # Alert when 80% spent
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Budget: {self.category.name} - {self.amount}"

    class Meta:
        unique_together = ['user', 'category', 'month', 'year']


class BudgetAlert(models.Model):
    ALERT_STATUS = [
        ('warning', 'Warning (80-99%)'),
        ('critical', 'Critical (100%+)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budget_alerts')
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ALERT_STATUS)
    spent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Alert: {self.budget.category.name} - {self.status}"

    class Meta:
        ordering = ['-created_at']


class MoneySavingQuote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=200, blank=True, null=True)
    emoji = models.CharField(max_length=10, default='💡')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.quote[:50]

    class Meta:
        ordering = ['?']  # Random order
