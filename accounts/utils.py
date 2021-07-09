import random
import string
import logging
import smtplib

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

logger = logging.getLogger(__name__)


def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def send_activation_mail(username, activation_code, receiver):
    ctx = {
        'username': username,
        'activation_code': activation_code
    }
    body = get_template('activation_mail.html').render(ctx)
    subject = 'Welcome to Yaari!, Please verify your account'
    send_mail(subject, body, [receiver])


def send_mail(subject, body, receiver):
    if not settings.EMAIL_ALLOWED:
        return logger.warning('Sending mail is not allowed')
    try:
        mail = EmailMultiAlternatives(
            subject=subject,
            body=body,
            to=receiver,
        )
        mail.attach_alternative(body, 'text/html')
        mail.send()
    except smtplib.SMTPAuthenticationError as e:
        logger.error(e.smtp_error)
