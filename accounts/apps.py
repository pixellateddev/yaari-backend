from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # noinspection PyUnresolvedReferences
    def ready(self):
        from . import signals
