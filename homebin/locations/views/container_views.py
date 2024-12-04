from typing import TYPE_CHECKING

from django.urls import reverse
from django.utils.translation import gettext_lazy as __
from iommi import EditTable, Form, html
from iommi.form import save_nested_forms

from homebin.attachments.models import GenericAttachment
from homebin.helpers.views import (
    BasePage,
    ItemBasePage,
    admin_button_class,
    item_label_class,
    item_row,
    item_row_class,
    project_thumbnail_aliases,
)
from homebin.locations import linebreaks  # , thumbnail_generator
from homebin.locations.models import Container
from homebin.locations.tables import ContainerCardTable
from homebin.locations.views.all_views import admin_container_change

if TYPE_CHECKING:
    from django.http import HttpRequest


def admin_container_changelist(request: "HttpRequest", **_):
    if not request.user.is_staff:
        return None

    return html.a(
        __("admin").title(),
        attrs__href=reverse("admin:locations_container_changelist"),
        attrs__class=admin_button_class,
    ).bind(request=request)


class ContainerListPage(BasePage):
    title = html.h1("Container List")
    actions = html.div(
        html.a(
            "Scan",
            attrs__href=lambda **_: reverse("container-scan"),
            attrs__class={"btn": True, "btn-info": True},
        ),
        admin_container_changelist,
        attrs__class={"btn-group": True},
    )
    containers_table = ContainerCardTable()


container_detail_preview_alias = alias = project_thumbnail_aliases.THUMBNAIL


class ContainerDetailPage(ItemBasePage):
    title = html.h1(lambda container, **_: container.label)
    actions = html.div(
        html.a(
            "List",
            attrs__href=lambda **_: reverse("container-list"),
            attrs__class={"btn": True, "btn-primary": True},
        ),
        admin_container_change,
        attrs__class={"btn-group": True},
        iommi_style="my_style",
    )
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
                        reverse(
                            "location-detail",
                            kwargs={"location_pk": container.location.pk},
                        )
                        if container.location
                        else ""
                    ),
                ),
                attrs__class=item_row_class,
            ),
            attrs__class={"list-group": True, "mt-3": True},
        )
    )
    attachments_title = html.h3("Attachments")

    class Meta:
        title = lambda container, **_: f"{container.label} | HomeBin"  # noqa: E731
        model = Container
        extra = {"label_field": "label"}


container_create_form = Form.create(auto__model=Container)

attachment_create_edit_table = EditTable(
    auto__model=GenericAttachment,
)


class ContainerCreateForm(Form):
    edit_container = Form.create(auto__model=Container)
    attachments = EditTable(auto__model=GenericAttachment)

    class Meta:
        actions__submit__post_handler = save_nested_forms


class ContainerCreatePage(BasePage):
    form = container_create_form
    attachments = attachment_create_edit_table
