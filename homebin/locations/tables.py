from typing import TYPE_CHECKING

from django_tables2 import columns, tables
from easy_thumbnails.files import get_thumbnailer
from iommi import Column, Table

from homebin.locations import linebreaks
from homebin.locations.models import Container, Location

if TYPE_CHECKING:
    from django.http import HttpRequest


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
        cell__value=lambda row, **_: get_thumbnailer_or_none(row.primary_image),
        cell__template="table_thumbnail.html",
    )

    class Meta:
        rows = Container.objects.all()
