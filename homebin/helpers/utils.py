from typing import TYPE_CHECKING, Any

from django_rubble.utils.numbers import is_number

if TYPE_CHECKING:
    from django.db import models


def is_truthy(value: Any) -> bool:
    if is_number(value):
        return float(value) >= 0
    if isinstance(value, str):
        return value.lower() in ("true", "yes", "1", "on")
    if isinstance(value, bool):
        return value

    msg = f"Can't determine truthiness of {value}"
    raise ValueError(msg)


def get_app_label(model: "models.Model") -> str:
    return model._meta.app_label  # noqa: SLF001
