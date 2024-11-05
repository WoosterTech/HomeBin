# Create your views here.
from django.urls import reverse
from easy_thumbnails.files import get_thumbnailer
from iommi import Page, html
from iommi.path import register_path_decoding

from homebin.assets.models import Asset, Manufacturer
from homebin.assets.tables import AssetTable, ManufacturerTable
from homebin.helpers.views import BasePage, item_label_class, item_row, item_row_class

register_path_decoding(manufacturer_slug=Manufacturer.slug, asset_pk=Asset)


class AssetListPage(BasePage):
    title = html.h1("Asset List")
    actions = html.div(
        html.a(
            "New",
            attrs__href=lambda **_: reverse("asset-create"),
            attrs__class={"btn": True, "btn-primary": True},
        ),
        html.a(
            "Edit (Admin)",
            attrs__href=lambda asset, **_: reverse("admin:assets_asset_change", args=[asset.pk]),
            attrs__class={"btn": True, "btn-secondary": True},
        ),
        attrs__class={"btn-group": True},
    )
    assets_table = AssetTable()


class AssetDetailPage(BasePage):
    title = html.h1(lambda asset, **_: asset.name)
    actions = html.div(
        html.a(
            "List",
            attrs__href=lambda **_: reverse("asset-list"),
            attrs__class={"btn": True, "btn-primary": True},
        ),
        html.a(
            "Admin",
            attrs__href=lambda **_: reverse("admin:assets_asset_changelist"),
            attrs__class={"btn": True, "btn-secondary": True},
        ),
        attrs__class={"btn-group": True},
    )
    primary_image = html.div(
        html.img(
            attrs__src=lambda asset, **_: get_thumbnailer(asset.primary_image)[
                "medium"
            ].url,
            attrs__alt=lambda asset, **_: asset.name,
        ),
    )
    asset = html.div(
        html.ul(
            html.li(
                html.span("Make: ", attrs__class=item_label_class),
                html.a(
                    lambda asset, **_: asset.make,
                    attrs__href=lambda asset, **_: reverse(
                        "manufacturer-detail",
                        kwargs={"manufacturer_slug": asset.make.slug},
                    ),
                ),
                attrs__class=item_row_class,
            ),
            item_row("Model", lambda asset, **_: asset.model),
            item_row("Serial Number", lambda asset, **_: asset.serial_number),
            item_row("Description", lambda asset, **_: asset.description),
            attrs__class={"list-group": True, "mt-3": True},
        )
    )


class ManufacturerListPage(BasePage):
    title = html.h1("Manufacturer List")
    actions = html.div(
        html.a(
            "New",
            attrs__href=lambda **_: reverse("admin:assets_manufacturer_add"),
            attrs__class={"btn": True, "btn-primary": True},
        ),
        attrs__class={"btn-group": True},
    )
    assets_table = ManufacturerTable()


class ManufacturerDetailPage(Page):
    title = html.h1(lambda manufacturer, **_: manufacturer.name)
    table_title = html.h3("Related Assets")
    related_assets = AssetTable(
        rows=lambda manufacturer, **_: manufacturer.asset_set.all(),
    )
