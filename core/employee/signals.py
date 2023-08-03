from django.db.models.signals import post_save
from django.dispatch import receiver
from core.account.models import User
from .models import Employee


@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(
            account=instance,
            employee=instance.username,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email
        )
