import logging
from typing import TYPE_CHECKING

import requests
from django.db.models import Q
from django.template import Template
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_rubble.utils.model_helpers import get_model_name
from django_tables2 import columns, tables
from easy_thumbnails.files import get_thumbnailer
from furl import furl
from iommi import Action, Column, Field, Table, html

from homebin.helpers.views import admin_button_class, get_thumbnail
from homebin.locations import collapsible_widget, linebreaks
from homebin.locations.models import Container, Location

if TYPE_CHECKING:
    from django.db import models
    from django.http import HttpRequest

logger = logging.getLogger(__name__)


class ContainerTable(tables.Table):
    label = columns.Column(linkify=True)

    class Meta:
        model = Container
        fields = ["label", "name", "description", "location"]
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-striped table-bordered table-hover"}
        empty_text = "No containers found"
        orderable = False
        per_page = 10


class LocationTable(tables.Table):
    name = columns.Column(linkify=True)

    class Meta:
        model = Location
        fields = ["name", "description", "parent_location"]
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-striped table-bordered table-hover"}
        empty_text = "No locations found"
        orderable = False
        per_page = 10


class LocationsTable(Table):
    name = Column(
        cell__url=lambda row, **_: row.get_absolute_url(),
        filter__include=True,
        filter__freetext=True,
    )
    description = Column(filter__include=True, filter__freetext=True)
    parent_location = Column.from_model(
        filter__include=True,
        filter__field__required=False,
        model=Location,
        model_field_name="parent_location",
    )

    class Meta:
        rows = Location.objects.all()


def get_thumbnailer_or_none(image_file):
    return get_thumbnailer(image_file)["thumbnail"] if image_file else None


def simple_contents(row: Container, request: "HttpRequest", **_):
    return linebreaks(request, container=row)


class ContainersTable(Table):
    label = Column(
        cell__url=lambda row, **_: row.get_absolute_url(),
        filter__include=True,
        filter__freetext=True,
        filter__field__include=False,
    )
    container_description = Column(filter__include=True, filter__freetext=True)
    simple_contents = Column(
        cell__value=simple_contents, filter__include=True, filter__freetext=True
    )
    location = Column.from_model(
        filter__include=True,
        filter__field__required=False,
        model=Container,
        model_field_name="location",
    )
    primary_image = Column(
        cell__value=lambda request, row, **_: (
            html.img(
                attrs__src=row.primary_thumbnail["avatar"].url,
                attrs__loading="lazy",
                attrs={"width": 100, "height": 100},
            ).bind(request=request)
            if row.primary_thumbnail
            else None
        ),
        cell__template="table_thumbnail.html",
    )

    class Meta:
        rows = Container.objects.all()


def get_unsplash_url(base_url: str | furl, client_id: str | None):
    base_url = furl(base_url) if isinstance(base_url, str) else base_url
    base_url = base_url / "photos/random/"
    full_url = base_url.add(
        query_params={
            "client_id": client_id,
            "query": "crate",
            "fit": "crop",
            "crop": "entropy",
            "w": 200,
            "h": 200,
        }
    )
    response = requests.get(full_url, timeout=10)
    return response.json()["urls"]["thumb"]


def card_linebreaks(request: "HttpRequest", row: "Container", **_):
    content_lines = row.simple_contents.split("\n")
    lines = [format_html("{}<br>", line) for line in content_lines]

    lines = collapsible_widget(lines, request.GET.copy())

    return html.div(*lines).bind(request=request)


def get_model_app(model: "models.Model") -> str:
    return model._meta.app_label  # noqa: SLF001


def get_changelist_url_lazy(model: "models.Model") -> str:
    return reverse_lazy(
        f"admin:{get_model_app(model)}_{get_model_name(model)}_changelist"
    )


scan_action = Action.button(
    display_name="Scan",
    attrs__href=reverse_lazy("container-scan"),
    attrs__class={"btn": True, "btn-info": True},
)
admin_changelist_action = Action.button(
    display_name="Admin",
    attrs__href=lambda user, table, **_: (
        get_changelist_url_lazy(table.rows.model) if user.is_staff else "#"
    ),
    attrs__class=admin_button_class,
    template=lambda user, **_: (
        Template("<a href='{{href}}' class='{{attrs__class}}'>{{display_name}}</a>")
        if not user.is_staff
        else None
    ),
)


class ContainerCardTable(Table):
    #select = Column.select()
    card = Column(
        cell__value=lambda request, row, **_: html.div(
            html.a(
                html.div(
                    html.img(
                        attrs__src=get_thumbnail(row.primary_thumbnail),
                        attrs__loading="lazy",
                        attrs={"width": 200, "height": 200},
                        attrs__class={"card-img": True},
                    ),
                    html.div(
                        html.h3(row.label, attrs__class__card_title=True),
                        html.p(row.location, attrs__class__card_text=True),
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
        ).bind(request=request),
    )
    label = Column(filter__include=True, filter__freetext=True, render_column=False)
    container_description = Column(
        filter__include=True, filter__freetext=True, render_column=False
    )
    location = Column.from_model(
        filter__include=True,
        filter__field__required=False,
        model=Container,
        model_field_name="location",
        choices=lambda **_: Location.active.active(),
        render_column=False,
        #bulk__include=True,
    )

    class Meta:
        rows = Container.objects.all()
        tag = "div"
        header__include = False
        query__form__fields__show_inactive = Field.boolean(
            initial=False,
            required=False,
            display_name=_("Show Inactive"),
        )
        query__form__fields__clear_filters = Action(
            display_name=_("Clear Filters"), attrs__href="?"
        )
        actions = {
            "scan": scan_action,
            "admin": admin_changelist_action,
        }

        @staticmethod
        def query__filters__show_inactive__value_to_q(value_string_or_f: str, **_):
            if value_string_or_f == "1":
                return Q()
            return Q(is_active=True)
