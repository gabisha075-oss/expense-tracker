from django.db.models import Sum
from decimal import Decimal
from datetime import datetime
from django.conf import settings
import logging

from .models import Expense, Budget, BudgetAlert

logger = logging.getLogger(__name__)


def send_sms(to_number: str, body: str) -> bool:
    """Send SMS using Twilio if enabled in settings. Returns True if sent."""
    if not getattr(settings, 'TWILIO_SMS_ENABLED', False):
        logger.debug('Twilio SMS not enabled or missing credentials; skipping SMS.')
        return False

    if not to_number:
        logger.debug('No phone number provided; skipping SMS.')
        return False

    try:
        from twilio.rest import Client
    except Exception as e:
        logger.exception('Twilio library not installed or import failed: %s', e)
        return False

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=body,
            from_=settings.TWILIO_FROM_NUMBER,
            to=to_number
        )
        logger.info('Sent SMS to %s; sid=%s', to_number, getattr(message, 'sid', None))
        return True
    except Exception as e:
        logger.exception('Failed to send SMS to %s: %s', to_number, e)
        return False


def check_budget_alerts(user, category, date):
    """Check if budget is exceeded and create alerts; optionally send SMS."""
    try:
        budget = Budget.objects.get(
            user=user,
            category=category,
            month=date.month,
            year=date.year
        )

        # Calculate spent amount
        spent = Expense.objects.filter(
            user=user,
            category=category,
            date__year=date.year,
            date__month=date.month
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')

        percentage = (spent / budget.amount * 100) if budget.amount > 0 else 0

        # Check if alert already exists (today)
        existing_alert = BudgetAlert.objects.filter(
            user=user,
            budget=budget,
            created_at__date=date
        ).exists()

        if not existing_alert:
            if percentage >= 100:
                alert = BudgetAlert.objects.create(
                    user=user,
                    budget=budget,
                    status='critical',
                    spent_amount=spent,
                    message=f"You have exceeded your {category.name} budget! Spent: ${spent}, Budget: ${budget.amount}"
                )
            elif percentage >= budget.alert_threshold:
                alert = BudgetAlert.objects.create(
                    user=user,
                    budget=budget,
                    status='warning',
                    spent_amount=spent,
                    message=f"You are approaching your {category.name} budget limit. {percentage:.1f}% spent (${spent}/{budget.amount})"
                )
            else:
                alert = None

            # Send SMS if alert created and user has phone and Twilio enabled
            if alert:
                try:
                    phone = getattr(user, 'profile', None) and getattr(user.profile, 'phone', '')
                    if phone:
                        sent = send_sms(phone, alert.message)
                        if not sent:
                            logger.debug('SMS not sent for alert id=%s', alert.id)
                except Exception:
                    logger.exception('Error while attempting to send SMS for budget alert')
    except Budget.DoesNotExist:
        pass


def generate_chart_data(expenses_by_category):
    """Generate chart data from expenses"""
    labels = [item['category__name'] for item in expenses_by_category]
    data = [float(item['total']) for item in expenses_by_category]
    colors = [item.get('category__color') or '#667eea' for item in expenses_by_category]

    return {
        'labels': labels,
        'data': data,
        'colors': colors,
    }
