from django.apps import AppConfig


class LocationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homebin.locations"

    def ready(self):
        from django.templatetags.static import static
        from iommi import Asset, Style, register_style
        from iommi.style import get_global_style

        bootstrap5 = get_global_style("bootstrap5")
        my_style = Style(
            bootstrap5,
            base_template="iommi_base.html",
            root__assets__project_css=Asset.css(
                attrs__src=lambda **_: static("css/project.css"),
            ),
        )

        register_style("my_style", my_style)
