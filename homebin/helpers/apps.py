from django import get_version
from django.apps import AppConfig


class HelpersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homebin.helpers"

    def ready(self):
        from django.templatetags.static import static
        from iommi import Asset, Style, register_style
        from iommi.style import get_global_style

        from homebin import __version__

        self.project_version = __version__
        self.django_version = get_version()

        bootstrap5 = get_global_style("bootstrap5")

        my_style = Style(
            bootstrap5,
            base_template="iommi_base.html",
            root__assets__project_css=Asset.css(
                attrs__href=lambda **_: static("css/project.css"),
                extra={"compress": True},
            ),
            root__assets__project_js=Asset.js(
                attrs__src=lambda **_: static("js/project.js"),
                extra={"compress": True},
            ),
            root__assets__iommi_js=Asset.js(
                attrs__src=lambda **_: static("js/iommi.js"),
                extra={"compress": True},
            ),
        )

        register_style("my_style", my_style)
