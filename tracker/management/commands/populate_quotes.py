from django.core.management.base import BaseCommand
from tracker.models import MoneySavingQuote

class Command(BaseCommand):
    help = 'Populate the database with money-saving quotes'

    def handle(self, *args, **options):
        quotes_data = [
            {
                'quote': 'A penny saved is a penny earned.',
                'author': 'Benjamin Franklin',
                'emoji': '💰'
            },
            {
                'quote': 'The best time to plant a tree was 20 years ago. The second best time is now.',
                'author': 'Chinese Proverb',
                'emoji': '🌱'
            },
            {
                'quote': 'Money is a great servant but a bad master.',
                'author': 'Francis Bacon',
                'emoji': '🎯'
            },
            {
                'quote': 'An investment in knowledge pays the best interest.',
                'author': 'Benjamin Franklin',
                'emoji': '📚'
            },
            {
                'quote': 'The more you save, the more you earn.',
                'author': 'Unknown',
                'emoji': '📈'
            },
            {
                'quote': 'Do not save money by going without food. Rather, save after you have eaten well.',
                'author': 'Jack Ma',
                'emoji': '🍴'
            },
            {
                'quote': 'Financial freedom is available to those who learn it and work for it.',
                'author': 'Robert Kiyosaki',
                'emoji': '🗽'
            },
            {
                'quote': 'Compound interest is the eighth wonder of the world.',
                'author': 'Albert Einstein',
                'emoji': '🔢'
            },
            {
                'quote': 'The key to making money is not to spend it.',
                'author': 'Unknown',
                'emoji': '🔑'
            },
            {
                'quote': 'Wealth consists not in having great possessions, but in having few wants.',
                'author': 'Unknown',
                'emoji': '✨'
            },
            {
                'quote': 'Your income can grow only to the extent that you do.',
                'author': 'T. Harv Eker',
                'emoji': '📊'
            },
            {
                'quote': 'Today is the best day to be smart about your money.',
                'author': 'Unknown',
                'emoji': '🧠'
            },
            {
                'quote': 'Money management is a life skill.',
                'author': 'Unknown',
                'emoji': '🎓'
            },
            {
                'quote': 'Save money. Money is power.',
                'author': 'Unknown',
                'emoji': '⚡'
            },
            {
                'quote': 'Spend less than you earn, and invest the difference.',
                'author': 'Unknown',
                'emoji': '📉'
            },
            {
                'quote': 'Financial peace is having both income and outgo under control.',
                'author': 'Dave Ramsey',
                'emoji': '☮️'
            },
        ]

        for quote_data in quotes_data:
            quote, created = MoneySavingQuote.objects.get_or_create(
                quote=quote_data['quote'],
                defaults={
                    'author': quote_data['author'],
                    'emoji': quote_data['emoji']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created quote: {quote_data["quote"][:50]}...'))
            else:
                self.stdout.write(f'Quote already exists: {quote_data["quote"][:50]}...')

        self.stdout.write(self.style.SUCCESS('Successfully populated quotes!'))
