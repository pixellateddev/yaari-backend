from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Verification, PasswordUtils
from .utils import generate_verification_code, send_activation_mail

import logging
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def generate_verification_instance_for_the_user(sender, instance, created, **kwargs):
    if created:
        PasswordUtils.objects.create(user=instance)
        if not instance.is_verified:
            logger.info(f'Creating verification for user {instance.username}')
            Verification.objects.create(user=instance, code=generate_verification_code())


@receiver(post_save, sender=Verification)
def send_activation_mail_to_the_user(sender, instance, created, **kwargs):
    logger.info(f'Sending activation mail for {instance.user.username}')
    send_activation_mail(instance.user.username, instance.code, instance.user.email)
