from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from tracker.models import Category

@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    """Create default expense and income categories when a user registers"""
    if created:
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
        
        for name, emoji in expense_categories:
            Category.objects.get_or_create(
                user=instance,
                name=name,
                category_type='expense',
                defaults={'emoji': emoji, 'color': '#667eea'}
            )
        
        # Create default income category
        Category.objects.get_or_create(
            user=instance,
            name='Salary',
            category_type='income',
            defaults={'emoji': '💵', 'color': '#27ae60'}
        )
        
        Category.objects.get_or_create(
            user=instance,
            name='Freelance',
            category_type='income',
            defaults={'emoji': '💻', 'color': '#3498db'}
        )
        
        Category.objects.get_or_create(
            user=instance,
            name='Bonus',
            category_type='income',
            defaults={'emoji': '🎁', 'color': '#f39c12'}
        )
