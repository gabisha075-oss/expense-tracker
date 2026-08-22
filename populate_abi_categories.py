#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')
django.setup()

from django.contrib.auth.models import User
from tracker.models import Category

user = User.objects.get(username='Abi')

# Delete old incomplete categories
Category.objects.filter(user=user).delete()

# Create default expense categories
expense_categories = [
    ('Food & Dining', '🍔'),
    ('Transportation', '🚗'),
    ('Shopping', '🛍️'),
    ('Entertainment', '🎬'),
    ('Utilities', '💡'),
    ('Healthcare', '⚕️'),
    ('Education', '📚'),
    ('Travel', '✈️'),
]

print('Creating expense categories...')
for name, emoji in expense_categories:
    cat = Category.objects.create(
        user=user,
        name=name,
        category_type='expense',
        emoji=emoji,
        color='#667eea'
    )
    print(f'  ✓ {emoji} {name}')

# Create default income categories
income_categories = [
    ('Salary', '💵'),
    ('Freelance', '💻'),
    ('Bonus', '🎁'),
]

print('\nCreating income categories...')
for name, emoji in income_categories:
    cat = Category.objects.create(
        user=user,
        name=name,
        category_type='income',
        emoji=emoji,
        color='#27ae60'
    )
    print(f'  ✓ {emoji} {name}')

print(f'\n✓ Total categories created: {Category.objects.filter(user=user).count()}')
