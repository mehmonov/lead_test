from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        from .views import create_attorney_group

        post_migrate.connect(lambda **kwargs: create_attorney_group(), sender=self)
