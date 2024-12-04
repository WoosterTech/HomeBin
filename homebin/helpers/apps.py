import sys

from django.apps import AppConfig


class HelpersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homebin.helpers"

    project_version: str | None = None
    django_version: str | None = None
    commit_hash: str | None = None
    python_version = None

    def ready(self):
        from django import get_version
        from django.templatetags.static import static
        from iommi import Asset, Style, register_style
        from iommi.style import get_global_style

        from homebin import __version__

        from . import get_git_commit_hash

        self.project_version = __version__
        self.django_version = get_version()
        self.python_version = sys.version_info

        self.commit_hash = get_git_commit_hash() or "unknown"

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
            Actions={
                "tag": "div",
                "attrs__class": {"btn-group": True, "links": False, "mb-3": True},
            },
        )

        register_style("my_style", my_style)

    @property
    def python_version_string(self):
        version_info = self.python_version or None
        if version_info is None:
            return "unknown"
        return f"{version_info.major}.{version_info.minor}.{version_info.micro}"
