from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Verification
from .utils import generate_verification_code


@receiver(post_save, sender=User)
def generate_verification_instance_for_the_user(_sender, instance, **_kwargs):
    if not instance.is_active:
        Verification.objects.create(user=instance, code=generate_verification_code())
