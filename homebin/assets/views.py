# Create your views here.
import logging

from iommi import Column, Field, Form, html
from iommi.path import register_path_decoding

from homebin.assets.models import Asset, Manufacturer
from homebin.assets.tables import AssetTable
from homebin.attachments.models import GenericAttachment
from homebin.attachments.tables import AttachmentImageTable
from homebin.helpers.forms import BaseForm
from homebin.helpers.views import (
    BaseTable,
    ItemBasePage,
    ItemImageBasePage,
    item_label_class,
    item_row,
    item_row_class,
    project_thumbnail_aliases,
)

logger = logging.getLogger(__name__)

register_path_decoding(
    manufacturer_slug=Manufacturer.slug, asset_pk=Asset, attachment_pk=GenericAttachment
)


def primary_thumbnail_or_none(request, asset: Asset | None, **_):
    if asset.primary_thumbnail is None or asset is None:
        return None
    return html.img(
        attrs__src=lambda asset, **_: asset.primary_thumbnail["medium"].url,
        attrs__alt=lambda asset, **_: asset.name,
    ).bind(request=request)


asset_detail_preview_alias = alias = project_thumbnail_aliases.THUMBNAIL


class AssetDetailPage(ItemImageBasePage):
    asset = html.div(
        html.ul(
            html.li(
                html.span("Make: ", attrs__class=item_label_class),
                html.a(
                    lambda asset, **_: asset.make,
                    attrs__href=lambda asset, **_: asset.make.get_absolute_url(),
                ),
                attrs__class=item_row_class,
            ),
            item_row("Model", lambda asset, **_: asset.model),
            item_row("Serial Number", lambda asset, **_: asset.serial_number),
            item_row("Description", lambda asset, **_: asset.description),
            html.li(
                html.span("Location: ", attrs__class=item_label_class),
                html.a(
                    lambda asset, **_: asset.location,
                    attrs__href=lambda asset, **_: (
                        asset.location.get_absolute_url() if asset.location else ""
                    ),
                ),
                attrs__class=item_row_class,
            ),
            html.li(
                lambda request, asset, **_: AttachmentImageTable(
                    rows=asset.attachments.filter(attachment_type="image")
                ).bind(request=request),
                attrs__class=item_row_class,
            ),
            html.li(
                BaseTable(
                    rows=lambda asset, **_: asset.attachments.images(not_images=True),
                    columns__name=Column.from_model(
                        model=GenericAttachment,
                        model_field_name="name",
                        cell__url=lambda row, **_: row.file.url,
                    ),
                    columns__attachment_type=Column(
                        filter__include=True,
                        cell__value=lambda row, **_: row.attachment_type.title(),
                    ),
                    title="Attachments",
                    actions=None,
                ),
                attrs__class=item_row_class,
                include=lambda asset, **_: asset.attachments.images(
                    not_images=True
                ).exists(),
            ),
            attrs__class={"list-group": True, "mt-3": True},
        )
    )

    class Meta:
        title = lambda asset, **_: f"{asset.name}"  # noqa: E731
        model = Asset
        extra = {"url_namespace": "assets"}


class AssetForm(BaseForm):
    class Meta:
        auto__model = Asset


asset_create_form = AssetForm.create()


asset_edit_form = AssetForm.edit(
    instance=lambda asset_pk, **_: Asset.objects.get(pk=asset_pk)
)

asset_delete_form = AssetForm.delete(
    instance=lambda asset_pk, **_: Asset.objects.get(pk=asset_pk)
)


class AssetAttachmentForm(Form):
    file = Field.file()
    attachment_type = Field.choice(
        choices=GenericAttachment.TYPE_CHOICES, initial="image"
    )

    class Meta:
        instance = lambda params, **_: GenericAttachment.objects.get(  # noqa: E731
            pk=params.attachment_pk
        )


class ManufacturerDetailPage(ItemBasePage):
    table_title = html.h3("Related Assets")
    related_assets = AssetTable(
        rows=lambda manufacturer, **_: manufacturer.asset_set.all(),
        actions=None,
    )

    class Meta:
        model = Manufacturer


class ManufacturerForm(Form):
    class Meta:
        auto__model = Manufacturer
        fields__slug__include = False


manufacturer_create_form = ManufacturerForm.create()


manufacturer_edit_form = ManufacturerForm.edit(
    instance=lambda manufacturer_slug, **_: Manufacturer.objects.get(
        slug=manufacturer_slug
    )
)

manufacturer_delete_form = ManufacturerForm.delete(
    instance=lambda manufacturer_slug, **_: Manufacturer.objects.get(
        slug=manufacturer_slug
    )
)
