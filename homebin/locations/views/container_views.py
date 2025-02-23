from iommi import Column, EditTable, Form, html

from homebin.attachments.models import GenericAttachment
from homebin.attachments.tables import AttachmentImageTable
from homebin.helpers.forms import BaseForm
from homebin.helpers.views import (
    BaseTable,
    ItemImageBasePage,
    item_label_class,
    item_row,
    item_row_class,
    project_thumbnail_aliases,
)
from homebin.locations import linebreaks
from homebin.locations.models import Container

container_detail_preview_alias = alias = project_thumbnail_aliases.THUMBNAIL


class ContainerDetailPage(ItemImageBasePage):
    title = html.h1(lambda container, **_: container.label)
    container = html.div(
        html.ul(
            item_row(
                "Description", lambda container, **_: container.container_description
            ),
            html.li(
                html.span("Contents: ", attrs__class=item_label_class),
                linebreaks,
                attrs__class=item_row_class,
            ),
            html.li(
                html.span("Location: ", attrs__class=item_label_class),
                html.a(
                    lambda container, **_: container.location,
                    attrs__href=lambda container, **_: (
                        container.location.get_absolute_url()
                        if container.location
                        else ""
                    ),
                ),
                attrs__class=item_row_class,
            ),
            html.li(
                lambda request, container, **_: AttachmentImageTable(
                    rows=container.attachments_generic.images()
                ).bind(request=request),
                attrs__class=item_row_class,
            ),
            html.li(
                BaseTable(
                    rows=lambda container, **_: (
                        container.attachments_generic.images(not_images=True)
                    ),
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
                include=lambda container, **_: (
                    container.attachments_generic.images(not_images=True).exists()
                ),
            ),
            attrs__class={"list-group": True, "mt-3": True},
        )
    )

    class Meta:
        title = lambda container, **_: f"Container {container.label}"  # noqa: E731
        model = Container
        extra = {"label_field": "label"}


container_create_form = Form.create(auto__model=Container)

attachment_create_edit_table = EditTable(
    auto__model=GenericAttachment,
)


class ContainerForm(BaseForm):
    class Meta:
        auto__model = Container


container_forms = ContainerForm.crud_form_factory()
