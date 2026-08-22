from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

try:
    import phonenumbers
except Exception:  # phonenumbers is optional until installed
    phonenumbers = None

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        """Normalize phone number to E.164 when possible before saving."""
        if self.phone and phonenumbers is not None:
            try:
                default_region = getattr(settings, 'DEFAULT_PHONE_REGION', 'US')
                parsed = phonenumbers.parse(self.phone, default_region)
                if phonenumbers.is_valid_number(parsed):
                    self.phone = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            except Exception:
                # If parsing fails, keep original value (no crash)
                pass

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "User Profiles"
