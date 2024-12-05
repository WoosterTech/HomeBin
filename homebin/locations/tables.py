import logging
from typing import TYPE_CHECKING

import requests
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_tables2 import columns, tables
from furl import furl
from iommi import Action, Column, Field, Table, html

from homebin.helpers.views import BaseTable, ItemImageTable
from homebin.locations import collapsible_widget, linebreaks
from homebin.locations.models import Container, Location

if TYPE_CHECKING:
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


class LocationsTable(BaseTable):
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
        title = "Location List"
        model = Location


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


scan_action = Action(
    display_name="Scan",
    attrs__href=reverse_lazy("container-scan"),
    attrs__class={"btn": True, "btn-info": True, "btn-secondary": False},
    attrs__role="button",
)


class ContainerCardTable(ItemImageTable):
    card_label_field = "label"
    label = Column(filter__include=True, filter__freetext=True, render_column=False)
    container_description = Column(
        filter__include=True, filter__freetext=True, render_column=False
    )
    simple_contents = Column(
        filter__include=True,
        filter__field__required=False,
        filter__freetext=True,
        render_column=False,
    )
    location = Column.from_model(
        filter__include=True,
        filter__field__required=False,
        model=Container,
        model_field_name="location__name",
        render_column=False,
        filter__freetext=True,
    )

    class Meta:
        title = "Container List"
        model = Container
        query__form__fields__show_inactive = Field.boolean(
            initial=False,
            required=False,
            display_name=_("Show Inactive"),
        )
        actions__scan = scan_action

        @staticmethod
        def query__filters__show_inactive__value_to_q(value_string_or_f: str, **_):
            if value_string_or_f == "1":
                return Q()
            return Q(is_active=True)
