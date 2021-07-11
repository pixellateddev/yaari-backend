from django.core import mail
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings


class Mailer:
    """
    Send email messages helper class
    """

    instances = {}

    @classmethod
    def get_instance(cls, from_email=settings.DEFAULT_FROM_EMAIL):
        if from_email in cls.instances:
            return cls.instances[from_email]
        cls.instances[from_email] = cls(from_email)
        return cls.instances[from_email]

    def __init__(self, from_email):
        self.connection = mail.get_connection()
        self.from_email = from_email

    def send_messages(self, subject, template, context, to_emails):
        if settings.EMAIL_ALLOWED:
            messages = self.__generate_messages(subject, template, context, to_emails)
            self.__send_mail(messages)

    def __send_mail(self, mail_messages):
        """
        Send email messages
        :param mail_messages:
        :return:
        """
        self.connection.open()
        self.connection.send_messages(mail_messages)
        self.connection.close()

    def __generate_messages(self, subject, template, context, to_emails):
        """
        Generate email message from Django template
        :param subject: Email message subject
        :param template: Email template
        :param to_emails: to email address[es]
        :return:
        """
        messages = []
        message_template = get_template(template)
        for recipient in to_emails:
            message_content = message_template.render(context)
            message = EmailMessage(subject, message_content, to=[recipient], from_email=self.from_email)
            message.content_subtype = 'html'
            messages.append(message)

        return messages


