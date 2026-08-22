#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')
django.setup()

from django.contrib.auth.models import User
from tracker.models import Category

user = User.objects.get(username='Abi')
cats = Category.objects.filter(user=user)

print(f'Total categories for Abi: {cats.count()}')
print(f'Income: {cats.filter(category_type="income").count()}')
print(f'Expense: {cats.filter(category_type="expense").count()}')
print('\nCategories:')
for c in cats:
    print(f'  - {c.name} ({c.category_type}) - {c.emoji}')
