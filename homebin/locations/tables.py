from typing import TYPE_CHECKING

import requests
from django.conf import settings
from django_tables2 import columns, tables
from easy_thumbnails.files import Thumbnailer, get_thumbnailer
from furl import furl
from iommi import Column, Table, html

from homebin.locations import linebreaks
from homebin.locations.models import Container, Location

if TYPE_CHECKING:
    from django.http import HttpRequest

UNSPLASH_ACCESS_KEY = settings.UNSPLASH_ACCESS_KEY or None
UNSPLASH_BASE_URL = settings.UNSPLASH_BASE_URL or None


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


def get_thumbnail(thumbnailer: Thumbnailer | None):
    if thumbnailer is not None:
        return thumbnailer["thumbnail"].url
    return get_unsplash_url(base_url=UNSPLASH_BASE_URL, client_id=UNSPLASH_ACCESS_KEY)


class ContainerCardTable(Table):
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
                    },
                    attrs__style__width="200px;",
                ),
                attrs__href=row.get_absolute_url(),
            ),
        ).bind(request=request)
    )
    label = Column(filter__include=True, filter__freetext=True, render_column=False)
    container_description = Column(
        filter__include=True, filter__freetext=True, render_column=False
    )
    location = Column(filter__include=True, filter__freetext=True, render_column=False)

    class Meta:
        rows = Container.objects.all()
