import random
import string
import logging

from app.utils import Mailer

logger = logging.getLogger(__name__)


def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def send_activation_mail(username, activation_code, receiver):
    ctx = {
        'username': username,
        'activation_code': activation_code
    }
    subject = 'Welcome to Yaari!, Please verify your account'
    mailer = Mailer('support@yaari.com')
    mailer.send_messages(
        subject=subject,
        template='activation_mail.html',
        context=ctx,
        to_emails=[receiver]
    )


def send_forgot_password_mail(username, forgot_password_code, receiver):
    ctx = {
        'username': username,
        'forgot_password_code': forgot_password_code
    }
    print(ctx)
    subject = 'Reset Password'
    mailer = Mailer('support@yaari.com')
    mailer.send_messages(
        subject=subject,
        template='forgot_password_mail.html',
        context=ctx,
        to_emails=[receiver]
    )