# Create your views here.
import logging
from collections.abc import Callable
from typing import Any

from django.db import models
from iommi import Fragment, Page, html

logger = logging.getLogger(__name__)


class BasePage(Page):
    title = html.h1(lambda page, **_: page.title.title())

    class Meta:
        title = "HomeBin"
        parts__h_tag__children = None


class IndexPage(BasePage):
    content = html.p("Welcome to HomeBin!")


item_label_class = {"fw-bold": True, "text-muted": True}
item_row_class = {"list-group-item": True}
admin_button_class = {"btn": True, "btn-secondary": True}


def item_row(
    label: str,
    value: Callable[[models.Model, Any], models.Model | str | Fragment],
):
    return html.li(
        html.span(f"{label}: ", attrs__class=item_label_class),
        value,
        attrs__class=item_row_class,
    )
