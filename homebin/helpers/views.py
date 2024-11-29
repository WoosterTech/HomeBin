# Create your views here.
import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.db import models
from iommi import Fragment, Page, html

if TYPE_CHECKING:
    from django.http import HttpRequest

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


thumbnail_aliases = settings.THUMBNAIL_ALIASES[""]


class Thumbnail:
    def _generate_thumbnail_func(
        self, model_path_name: str, field_name: str, thumbnail_size: str
    ):
        width, height = thumbnail_aliases[thumbnail_size]["size"]

        def get_thumbnail(request: "HttpRequest", **kwargs):
            model = kwargs.get(model_path_name)
            image = getattr(model, field_name, None)
            if image is None:
                return None

            def url(**kwargs):
                model = kwargs.get(model_path_name)
                image = getattr(model, field_name)
                return image[thumbnail_size].url

            def label(**kwargs):
                model = kwargs.get(model_path_name)
                return model.label

            return html.img(
                attrs__src=url,
                attrs__alt=label,
                attrs__loading="lazy",
                attrs={"width": width, "height": height},
            ).bind(request=request)

        return get_thumbnail

    def thumbnail_func(
        self, model_path_name: str, field_name: str, thumbnail_size: str
    ) -> Callable[..., Fragment | None]:
        method_name = f"get_{model_path_name}_{field_name}_{thumbnail_size}_thumbnail"
        if hasattr(self, method_name):
            return getattr(self, method_name)

        setattr(
            self,
            method_name,
            self._generate_thumbnail_func(model_path_name, field_name, thumbnail_size),
        )

        return getattr(self, method_name)
