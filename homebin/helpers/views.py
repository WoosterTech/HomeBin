# Create your views here.
import logging
from collections.abc import Callable
from enum import Enum
from gettext import gettext as _
from typing import TYPE_CHECKING, Any, Literal, NamedTuple

from django.conf import settings
from django.urls import reverse
from django_rubble.utils.model_helpers import get_model_name
from furl import furl
from iommi import Action, Asset, Column, Fragment, Page, Table, html
from iommi.refinable import SpecialEvaluatedRefinable
from pydantic import BaseModel

if TYPE_CHECKING:
    from django.db import models
    from django.http import HttpRequest
    from easy_thumbnails.files import Thumbnailer

    from homebin.helpers.models import ItemBaseModel

logger = logging.getLogger(__name__)


item_label_class = {"fw-bold": True, "text-muted": True}
item_row_class = {"list-group-item": True}
admin_button_class = {"btn": True, "btn-secondary": True}


class BasePage(Page):
    title = html.h1(lambda page, **_: page.title.title())

    class Meta:
        title = "HomeBin"
        parts__h_tag__children = None


class BaseAction(Action):
    attrs__role = "button"


admin_changelist_action = BaseAction(
    display_name=_("Admin"),
    attrs__href=lambda table, **_: (table.rows.model.objects.admin_changelist_url()),
    attrs__class=admin_button_class,
    include=lambda user, **_: user.is_staff,
    after=99,
)

admin_change_action = BaseAction(
    display_name=_("Admin"),
    attrs__href=lambda page, **kwargs: get_model_instance(page)(
        **kwargs
    ).get_admin_change_url(),
    attrs__class=admin_button_class,
    include=lambda user, **_: user.is_staff,
)


def get_model_instance(page):
    model_name = get_model_name(page.model)
    return lambda **kwargs: kwargs.get(model_name)


class ItemBasePage(BasePage):
    model: "type[models.Model]" = SpecialEvaluatedRefinable()
    actions = html.div(
        BaseAction(
            display_name=_("Edit"),
            attrs__href=lambda page, **kwargs: reverse(
                f"{get_model_name(page.model)}-edit",
                args=[
                    getattr(get_model_instance(page)(**kwargs), page.model.lookup_field)
                ],
            ),
            attrs__class={"btn": True, "btn-success": True, "btn-secondary": False},
            include=lambda user, page, **_: user.has_perm(
                f"{get_model_name(page.model)}.change"
            ),
        ),
        BaseAction(
            display_name="List",
            attrs__href=lambda page, **_: reverse(f"{get_model_name(page.model)}-list"),
            attrs__class={"btn": True, "btn-primary": True, "btn-secondary": False},
        ),
        admin_change_action,
        attrs__class={"btn-group": True},
    )

    class Meta:
        extra = {"label_field": "name"}


class ItemImageBasePage(ItemBasePage):
    primary_image = html.div(
        lambda request, page, **kwargs: (
            html.a(
                html.img(
                    attrs__src=alias.get_primary_thumbnail(
                        instance := get_model_instance(page)(**kwargs)
                    ),
                    attrs__class={"img-thumbnail": True, "img-fluid": True},
                    attrs__loading="lazy",
                    attrs={"width": alias.width, "height": alias.height},
                ),
                attrs={
                    "href": (
                        instance.primary_image.url if instance.primary_image else "#"
                    ),
                    "data-lightbox": "primary-thumbnail",
                    "data-alt": getattr(instance, page.extra["label_field"]),
                },
            ).bind(request=request)
            if get_model_instance(page)(**kwargs).primary_thumbnail is not None
            else None
        ),
        attrs__class={"mt-3": True},
    )

    class Meta:
        assets = {
            "lightbox2_js": Asset.js(
                attrs={
                    "src": "https://cdn.jsdelivr.net/npm/lightbox2@2.11.5/dist/js/lightbox.min.js",
                    "integrity": "sha384-bcXRY0im+IjB6RvmBpbgdkqjLV0pCTbaJRJ9IRPeQaWCYlzRn9pPaPmCvONr9h9z",  # noqa: E501
                    "crossorigin": "anonymous",
                }
            ),
            "lightbox2_css": Asset.css(
                attrs={
                    "href": "https://cdn.jsdelivr.net/npm/lightbox2@2.11.5/dist/css/lightbox.min.css",
                    "integrity": "sha384-9623XJODy0qDAl6X6Y9xTBSzYUxM0ixdjO8zqJQeGzDP2Uwo1PqAOq6gXkk2ul99",  # noqa: E501
                    "crossorigin": "anonymous",
                }
            ),
        }


create_new_action = BaseAction(
    display_name=_("New"),
    attrs__href=lambda table, **_: reverse(f"{get_model_name(table.model)}-create"),
    attrs__class={"btn": True, "btn-success": True, "btn-secondary": False},
    include=lambda user, table, **_: user.has_perm(
        f"{get_model_name(table.model)}.add"
    ),
    after=-1,
)


class BaseTable(Table):
    title = html.h1(lambda table, **_: table.title.title())

    class Meta:
        title = "Table"
        parts__h_tag__children = None
        actions__create_new = create_new_action
        actions__admin = admin_changelist_action
        query__form__fields__clear_filters = Action(
            display_name=_("Clear Filters"),
            attrs__href="?",
            after=99,
        )


class IndexPage(BasePage):
    content = html.p("Welcome to HomeBin!")


thumbnail_aliases = settings.THUMBNAIL_ALIASES[""]
empty_thumbnail_url = furl("https://placehold.co/200x200/grey/white/svg?text=empty")


class ImgSize(NamedTuple):
    width: int
    height: int


class ThumbnailAlias(BaseModel):
    size: ImgSize
    crop: Literal["smart"]

    @property
    def width(self) -> int:
        return self.size.width

    @property
    def height(self) -> int:
        return self.size.height


class ThumbnailAliases(Enum):
    @property
    def alias(self) -> str:
        return self.name.lower()

    @property
    def width(self) -> int:
        return self.value.width

    @property
    def height(self) -> int:
        return self.value.height

    def get_row_primary_thumbnail(self, row: "models.Model") -> str:
        return (
            row.primary_thumbnail[self.alias].url
            if row.primary_thumbnail
            else empty_thumbnail_url.url
        )

    def get_primary_thumbnail(self, instance: "ItemBaseModel") -> str:
        return (
            instance.primary_thumbnail[self.alias].url
            if instance.primary_thumbnail
            else empty_thumbnail_url.url
        )

    def __getattr__(self, name: str, **kwargs):
        if name.startswith("get__") and name.endswith("__primary_thumbnail"):
            parameter_name = name.split("__")[1]
            return lambda **kwargs: (
                kwargs.get(parameter_name).primary_thumbnail[self.alias].url
                if kwargs.get(parameter_name).primary_thumbnail
                else empty_thumbnail_url.url
            )
        msg = f"ThumbnailAliases has no attribute {name}"
        raise AttributeError(msg)


def initialize_thumbnail_aliases(
    name: str, thumbnail_aliases: dict[str, str | ImgSize]
):
    alias_dict = {}
    for alias, alias_params in thumbnail_aliases.items():
        alias_dict[alias.upper()] = ThumbnailAlias.model_validate(alias_params)
    return ThumbnailAliases(name, alias_dict)


project_thumbnail_aliases = initialize_thumbnail_aliases(
    "ThumbnailAliases", thumbnail_aliases
)


alias = project_thumbnail_aliases.THUMBNAIL


class ItemImageTable(BaseTable):
    card_label_field = "name"
    card_sub_text_field = "location"
    card = Column(
        cell__value=lambda request, row, table, **_: html.div(
            html.a(
                html.div(
                    html.img(
                        attrs__src=alias.get_primary_thumbnail(row),
                        attrs__loading="lazy",
                        attrs={"width": alias.width, "height": alias.height},
                        attrs__class={"card-img": True},
                    ),
                    html.div(
                        html.h3(
                            getattr(row, table.card_label_field),
                            attrs__class__card_title=True,
                        ),
                        html.p(
                            getattr(row, table.card_sub_text_field),
                            attrs__class__card_text=True,
                        ),
                        attrs__class={"card-img-overlay": True},
                    ),
                    attrs__class={
                        "card": True,
                        "text-center": True,
                        "text-white": True,
                        "bg-dark": True,
                        "col-sm-12": True,
                    },
                ),
                attrs__href=row.get_absolute_url(),
            ),
            attrs__style__display="inline-block",
        ).bind(request=request)
    )

    class Meta:
        tag = "div"
        header__include = False


def item_row(
    label: str,
    value: Callable[["models.Model", Any], "models.Model | str | Fragment"],
):
    return html.li(
        html.span(f"{label}: ", attrs__class=item_label_class),
        value,
        attrs__class=item_row_class,
    )


def get_thumbnail(thumbnailer: "Thumbnailer | None") -> str:
    if thumbnailer is not None:
        return thumbnailer["thumbnail"].url
    return empty_thumbnail_url.url


class ThumbnailFuncEnum:
    def __getattr__(
        self,
        name: str,
        container: "models.Model | None" = None,
        **_,
    ):
        if name.startswith("get__"):
            name_parts = name.split("__")
            name_parts_len = len(name_parts)
            expected_parts_len = 3
            if name_parts_len < expected_parts_len:
                msg = f"AttributeError: 'ThumbnailFuncEnum' object has no attribute '{name}'"  # noqa: E501
                raise AttributeError(msg)
            alias = (
                name_parts[-1] if name_parts_len == expected_parts_len else "thumbnail"
            )

            if container.primary_thumbnail is None:
                logger.debug("Thumbnail locals(): %s", locals())
                return lambda **_: self._get_empty_thumbnail(alias)

            return lambda **_: self._get_thumbnail(container.primary_thumbnail, alias)

        msg = f"AttributeError: 'ThumbnailFuncEnum' object has no attribute '{name}'"
        raise AttributeError(msg)

    def _get_thumbnail(self, thumbnailer: "Thumbnailer", alias: str) -> str:
        return thumbnailer[alias].url

    def _get_empty_thumbnail(self, alias: str, **_) -> str:
        empty_furl = furl("https://placehold.co")
        logger.debug("Thumbnail alias %s: %s", alias, thumbnail_aliases[alias])
        width, height = thumbnail_aliases[alias]["size"]
        # TODO: add support for more configurable params
        text = "empty"
        bg_color = "grey"
        text_color = "white"
        file_format = "svg"
        empty_furl.add(path=f"{width}x{height}/{bg_color}/{text_color}/{file_format}")
        empty_furl.add(args={"text": text})
        return empty_furl.url


get_thumbnails = ThumbnailFuncEnum()


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

    def card(self, request: "HttpRequest", instance: "models.Model", **kwargs):
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

    def _image(self, request: "HttpRequest", instance: "models.Model", **_):
        return html.img(
            attrs__src=get_thumbnail(instance.primary_thumbnail),
            attrs__loading=self.loading,
            attrs={"width": self.width, "height": self.height},
            attrs__class={"card-img": True},
        ).bind(request=request)

    def _sub_text(self, request: "HttpRequest", instance: "models.Model", **_):
        field_value = getattr(instance, self.sub_text_field)
        return html.p(field_value, attrs__class__card_text=True).bind(request=request)
