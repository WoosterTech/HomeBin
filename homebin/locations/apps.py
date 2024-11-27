from django.apps import AppConfig


class LocationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homebin.locations"

    def ready(self):
        from django.contrib.staticfiles.storage import staticfiles_storage
        from iommi import Asset, Style, register_style
        from iommi.style import get_global_style

        static_prefix = staticfiles_storage.url("")
        bootstrap5 = get_global_style("bootstrap5")
        my_style = Style(
            bootstrap5,
            base_template="iommi_base.html",
            root__assets__project_css=Asset.css(
                attrs__href=f"{static_prefix}css/project.css",
                attrs__rel="stylesheet",
            ),
        )

        register_style("my_style", my_style)
