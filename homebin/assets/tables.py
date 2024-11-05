from easy_thumbnails.files import get_thumbnailer
from iommi import Column, Table

from homebin.assets.models import Asset, Manufacturer


class ManufacturerTable(Table):
    name = Column(cell__url=lambda row, **_: row.get_absolute_url())

    class Meta:
        rows = Manufacturer.objects.all()


class AssetTable(Table):
    name = Column(cell__url=lambda row, **_: row.get_absolute_url())
    make = Column(filter__include=True)
    model = Column()
    serial_number = Column()
    primary_image = Column(
        cell__value=lambda row, **_: get_thumbnailer(row.primary_image)["thumbnail"],
        cell__template="table_thumbnail.html",
    )

    class Meta:
        rows = Asset.objects.all()