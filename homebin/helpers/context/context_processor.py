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

    version_info = app.python_version_string
    current_year = now().year

    return {
        "PROJECT_VERSION": app.project_version,
        "COMMIT_HASH": app.commit_hash,
        "DJANGO_VERSION": app.django_version,
        "PYTHON_VERSION": (version_info),
        "COPYRIGHT": (
            format_html(
                "Author: <a href='mailto:karl@woostertech.com?subject=HomeBin'>"
                "Karl Wooster</a> ©{}"
                " <a href='https://woostertech.com'>Wooster Technical Solutions</a>",
                current_year,
            )
        ),
    }
