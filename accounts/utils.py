import random
import string
import logging

from app.utils import Mailer

mailer = Mailer()
logger = logging.getLogger(__name__)


def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def send_activation_mail(username, activation_code, receiver):
    ctx = {
        'username': username,
        'activation_code': activation_code
    }
    subject = 'Welcome to Yaari!, Please verify your account'
    mailer.send_messages(
        subject=subject,
        template='activation_mail.html',
        context=ctx,
        to_emails=[receiver]
    )
