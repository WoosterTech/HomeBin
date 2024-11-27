from django import get_version
from django.apps import AppConfig


class HelpersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homebin.helpers"

    def ready(self):
        from homebin import __version__

        self.project_version = __version__
        self.django_version = get_version()
