#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')
django.setup()

from django.contrib.auth.models import User
from tracker.models import Category
from accounts.models import UserProfile

print('Normalizing phones for users with profiles...')
count = 0
for profile in UserProfile.objects.exclude(phone__isnull=True).exclude(phone__exact=''):
    old = profile.phone
    profile.save()
    print(f"{profile.user.username}: '{old}' -> '{profile.phone}'")
    count += 1

print(f"Done. Profiles processed: {count}")
