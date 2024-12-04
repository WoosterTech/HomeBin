from iommi import Column, Table

from homebin.assets.models import Asset, Manufacturer
from homebin.helpers.views import ItemImageTable


class ManufacturerTable(Table):
    name = Column(cell__url=lambda row, **_: row.get_absolute_url())

    class Meta:
        rows = Manufacturer.objects.all()


class AssetTable(ItemImageTable):
    name = Column(filter__include=True, filter__freetext=True, render_column=False)
    manufacturer = Column.from_model(
        filter__include=True,
        filter__freetext=True,
        render_column=False,
        model=Asset,
        model_field_name="make__name",
    )
    description = Column(
        filter__include=True, filter__freetext=True, render_column=False
    )

    class Meta:
        title = "Asset List"
        rows = Asset.objects.all()
