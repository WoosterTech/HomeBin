# Create your views here.
import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Literal

from django.conf import settings
from django.db import models
from furl import furl
from iommi import Fragment, Page, html
from pydantic import BaseModel

if TYPE_CHECKING:
    from django.http import HttpRequest
    from easy_thumbnails.files import Thumbnailer

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
empty_thumbnail_url = furl("https://placehold.co/200x200/grey/white/svg?text=empty")


def get_thumbnail(thumbnailer: "Thumbnailer | None"):
    if thumbnailer is not None:
        return thumbnailer["thumbnail"].url
    return empty_thumbnail_url


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


class CardDefinition(BaseModel):
    width: int = 200
    height: int = 200
    loading: Literal["lazy", "eager"] = "lazy"
    overlay: bool = True
    card_classes: list[str] = ["text-center", "text-white", "bg-dark"]
    extend_card_classes: list[str] | None = None
    sub_text_field: str

    def card(self, request: "HttpRequest", instance: models.Model, **kwargs):
        card_classes = self.card_classes
        if self.extend_card_classes is not None:
            card_classes += self.extend_card_classes
        return html.div(
            html.img(
                attrs__src=get_thumbnail(instance.primary_thumbnail),
                attrs__loading=self.loading,
                attrs={"width": self.width, "height": self.height},
                attrs__class={"card-img": True},
            ).bind(request=request),
            html.div(
                html.h3(instance.label, attrs__class__card_title=True),
                html.p(instance.location, attrs__class__card_text=True),
                attrs__class={"card-img-overlay": self.overlay},
            ).bind(request=request),
            attrs__class={"card": True, **{key: True for key in card_classes}},
        ).bind(request=request)

    def _image(self, request: "HttpRequest", instance: models.Model, **_):
        return html.img(
            attrs__src=get_thumbnail(instance.primary_thumbnail),
            attrs__loading=self.loading,
            attrs={"width": self.width, "height": self.height},
            attrs__class={"card-img": True},
        ).bind(request=request)

    def _sub_text(self, request: "HttpRequest", instance: models.Model, **_):
        field_value = getattr(instance, self.sub_text_field)
        return html.p(field_value, attrs__class__card_text=True).bind(request=request)
