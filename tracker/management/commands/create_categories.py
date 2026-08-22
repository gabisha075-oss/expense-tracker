from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Category

class Command(BaseCommand):
    help = 'Create default categories for users who do not have any'

    def handle(self, *args, **options):
        users = User.objects.all()
        
        default_expense_categories = [
            ('Food & Dining', '🍔'),
            ('Transportation', '🚗'),
            ('Shopping', '🛍️'),
            ('Entertainment', '🎬'),
            ('Utilities', '💡'),
            ('Healthcare', '⚕️'),
            ('Education', '📚'),
            ('Travel', '✈️'),
        ]
        
        default_income_categories = [
            ('Salary', '💵'),
            ('Freelance', '💻'),
            ('Bonus', '🎁'),
        ]
        
        for user in users:
            # Check if user has any categories
            if not Category.objects.filter(user=user).exists():
                self.stdout.write(f'Creating categories for {user.username}...')
                
                # Create expense categories
                for name, emoji in default_expense_categories:
                    Category.objects.create(
                        user=user,
                        name=name,
                        category_type='expense',
                        emoji=emoji,
                        color='#667eea'
                    )
                
                # Create income categories
                for name, emoji in default_income_categories:
                    Category.objects.create(
                        user=user,
                        name=name,
                        category_type='income',
                        emoji=emoji,
                        color='#27ae60'
                    )
                
                self.stdout.write(self.style.SUCCESS(f'✓ Categories created for {user.username}'))
            else:
                self.stdout.write(f'User {user.username} already has categories')
