import sys

from django.apps import apps
from django.utils.html import format_html
from django.utils.timezone import now

from homebin.helpers.apps import HelpersConfig


class InvalidConfigError(Exception):
    pass


def site_config(*_):
    """Get configuration of project for menus."""
    app = apps.get_app_config("helpers")
    if not isinstance(app, HelpersConfig):
        raise InvalidConfigError

    version_info = sys.version_info
    current_year = now().year

    return {
        "PROJECT_VERSION": app.project_version,
        "DJANGO_VERSION": app.django_version,
        "PYTHON_VERSION": (
            f"{version_info.major}.{version_info.minor}.{version_info.micro}_{version_info.releaselevel}"
        ),
        "COPYRIGHT": (
            format_html(
                "Author: <a href='mailto:karl@woostertech.com?subject=HomeBin'>"
                "Karl Wooster</a> ©{}"
                " <a href='https://woostertech.com'>Wooster Technical Solutions</a>",
                current_year,
            )
        ),
    }
