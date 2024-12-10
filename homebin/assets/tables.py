from iommi import Column

from homebin.assets.models import Asset, Manufacturer
from homebin.helpers.views import BaseTable, ItemImageTable


class ManufacturerTable(BaseTable):
    name = Column(
        cell__url=lambda row, **_: row.get_absolute_url(),
        filter__include=True,
        filter__freetext=True,
    )

    class Meta:
        title = "Manufacturer List"
        model = Manufacturer


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
        model = Asset
        extra = {"url_namespace": "assets"}
