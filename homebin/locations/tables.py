from django_tables2 import columns, tables
from easy_thumbnails.files import get_thumbnailer
from iommi import Column, Table

from homebin.locations.models import Container, Location


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
    name = Column(cell__url=lambda row, **_: row.get_absolute_url())
    description = Column()
    parent_location = Column()

    class Meta:
        rows = Location.objects.all()


def get_thumbnailer_or_none(image_file):
    return get_thumbnailer(image_file)["thumbnail"] if image_file else None


class ContainersTable(Table):
    label = Column(cell__url=lambda row, **_: row.get_absolute_url())
    container_description = Column()
    simple_contents = Column()
    location = Column()
    primary_image = Column(
        cell__value=lambda row, **_: get_thumbnailer_or_none(row.primary_image),
        cell__template="table_thumbnail.html",
    )

    class Meta:
        rows = Container.objects.all()
