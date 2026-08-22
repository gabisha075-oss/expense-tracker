from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Budget, BudgetAlert
from tracker.utils import send_sms
from django.utils import timezone

class Command(BaseCommand):
    help = 'Send a test SMS alert to a user (if Twilio configured and phone set)'

    def add_arguments(self, parser):
        parser.add_argument('username', help='Username to send test alert to')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist'))
            return

        # Construct a test message
        message = 'This is a test budget alert from ExpenseTracker. If configured, this will arrive as SMS.'

        phone = getattr(user, 'profile', None) and getattr(user.profile, 'phone', '')
        if not phone:
            self.stdout.write(self.style.WARNING(f'User {username} has no phone number set on profile'))
            return

        sent = send_sms(phone, message)
        if sent:
            self.stdout.write(self.style.SUCCESS(f'SMS sent to {phone}'))
        else:
            self.stdout.write(self.style.ERROR('SMS not sent. Check TWILIO settings and Twilio package installation.'))
