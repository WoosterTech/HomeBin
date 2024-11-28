# Create your views here.
import logging
from typing import TYPE_CHECKING

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as __
from django_tables2 import SingleTableView
from iommi import Field, Form, html
from iommi.path import register_path_decoding
from iommi.style import resolve_style

from homebin.assets.tables import AssetTable
from homebin.helpers.views import (
    BasePage,
    admin_button_class,
    item_label_class,
    item_row,
    item_row_class,
)
from homebin.locations import linebreaks
from homebin.locations.models import Container, Location
from homebin.locations.tables import (
    ContainersTable,
    ContainerTable,
    LocationsTable,
    LocationTable,
)

if TYPE_CHECKING:
    from django.http import HttpRequest

logger = logging.getLogger(__name__)

register_path_decoding(container_label=Container.label, location_pk=Location)

MAX_CONTENT_LINES = 5


def primary_thumbnail_or_none(
    request: "HttpRequest", container: "Container | None", **_
):
    if container.primary_thumbnail is None:
        logger.info("No primary image for %s", container)
        return None
    logger.info("Primary image for %s is %s", container, container.primary_thumbnail)
    return html.img(
        attrs__src=lambda container, **_: container.primary_thumbnail["medium"].url,
        attrs__alt=lambda container, **_: container.label,
    ).bind(request=request)


class LocationListPage(BasePage):
    title = html.h1("Location List")
    actions = html.div(
        html.a(
            "New",
            attrs__href=lambda **_: reverse("location-create"),
            attrs__class={"btn": True, "btn-primary": True},
        ),
        html.a(
            "Admin",
            attrs__href=lambda **_: reverse("admin:locations_location_changelist"),
            attrs__class={"btn": True, "btn-secondary": True},
        ),
        attrs__class={"btn-group": True},
    )
    locations_table = LocationsTable()


def location_detail_actions(location, request, **_):
    logger.debug("location_detail_actions %s", location)
    if location.parent_location:

        def attrs_href(location, **_):
            return location.parent_location.get_absolute_url()

        return html.a(
            lambda location, **_: f"Up to {location.parent_location}",
            attrs__href=attrs_href,
        ).bind(request=request)

    return None


def breadcrumbs_link(request: "HttpRequest", location: Location, **kwargs):
    logger.warning("breadcrumbs_link: %s", location)
    breadcrumbs = reversed(location.breadcrumbs())
    ol_list = [
        html.li(
            (
                html.a(
                    crumb.name.title(),
                    attrs__href=reverse(
                        "location-detail", kwargs={"location_pk": crumb.pk}
                    ),
                )
                if crumb != location
                else crumb.name.title()
            ),
            attrs__class={"breadcrumb-item": True},
            attrs__aria_current="page" if crumb == location else None,
        )
        for crumb in breadcrumbs
    ]

    return html.ol(
        *ol_list,
        attrs__class={"breadcrumb": True},
    ).bind(request=request)


class LocationDetailPage(BasePage):
    breadcrumbs = html.nav(breadcrumbs_link, attrs__aria_label="breadcrumb")
    title = html.h1(lambda location, **_: location.name)

    actions = html.div(
        html.a(
            "List",
            attrs__href=lambda **_: reverse("location-list"),
            attrs__class={"btn": True, "btn-primary": True},
        ),
        html.a(
            "Admin",
            attrs__href=lambda **_: reverse("admin:locations_location_changelist"),
            attrs__class={"btn": True, "btn-secondary": True},
        ),
        attrs__class={"btn-group": True},
    )

    sub_locations_table_title = html.h3("Sub Locations")
    sub_locations = LocationsTable(
        rows=lambda location, **_: location.location_set.all(),
    )

    table_title = html.h3("Related Containers")
    related_containers = ContainersTable(
        rows=lambda location, **_: location.containers.all()
    )

    asset_table_title = html.h3("Related Assets")
    related_assets = AssetTable(
        rows=lambda location, **_: location.asset_set.all(),
    )


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
            "New",
            attrs__href=lambda **_: reverse("container-create"),
            attrs__class={"btn": True, "btn-primary": True},
        ),
        html.a(
            "Scan",
            attrs__href=lambda **_: reverse("container-scan"),
            attrs__class={"btn": True, "btn-info": True},
        ),
        admin_container_changelist,
        attrs__class={"btn-group": True},
    )
    containers_table = ContainersTable()


def row_with_link(label, field_object, **kwargs):
    return (
        html.span(f"{label}: ", attrs__class=item_label_class),
        html.a(
            field_object,
            attrs__href=field_object.get_absolute_url(),
        ),
    )


def admin_container_change(request: "HttpRequest", container: "Container", **_):
    if not request.user.is_staff:
        return None

    return html.a(
        __("admin").title(),
        attrs__href=reverse("admin:locations_container_change", args=[container.pk]),
        attrs__class=admin_button_class,
    ).bind(request=request)


IOMMI_STYLE = resolve_style("my_style")


class ContainerDetailPage(BasePage):
    title = html.h1(lambda container, **_: container.label)
    actions = html.div(
        html.a(
            "Edit",
            attrs__href=lambda container, **_: reverse(
                "container-edit", kwargs={"container_label": container.label}
            ),
            attrs__class={"btn": True, "btn-primary": True},
        ),
        html.a(
            "List",
            attrs__href=lambda **_: reverse("container-list"),
            attrs__class={"btn": True, "btn-primary": True},
        ),
        admin_container_change,
        attrs__class={"btn-group": True},
        iommi_style="my_style",
    )
    primary_image = html.div(primary_thumbnail_or_none, attrs__loading=True, attrs={"width": "200","height": "200"}, attrs__class={"mt-3": True})
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
    # TODO: attachments = AttachmentsTable()


def container_detail(request: "HttpRequest", label: str):
    container = Container.objects.get(label=label)
    context = {"object": container}

    return render(request, "locations/container_detail.html", context)


class ContainerListView(SingleTableView):
    model = Container
    table_class = ContainerTable
    template_name = "locations/container_list.html"


def location_detail(request: "HttpRequest", pk: int):
    location = Location.objects.get(pk=pk)
    context = {"object": location}

    return render(request, "locations/location_detail.html", context)


class LocationListView(SingleTableView):
    model = Location
    table_class = LocationTable
    template_name = "base_list.html"


def breadcrumb_test(request: "HttpRequest", pk: int):
    location = Location.objects.get(pk=pk)
    return HttpResponse(
        f"Breadcrumbs are {[loc.name for loc in location.breadcrumbs()]}"
    )


class ContainerQueryForm(Form):
    label = Field.text(input__attrs__placeholder="e.g. 5BK4J")

    class Meta:
        @staticmethod
        def actions__submit__post_handler(request: "HttpRequest", form: Form, **_):
            if form.is_valid():
                try:
                    container = Container.objects.get(label=form.fields["label"].value)
                except Container.DoesNotExist:
                    messages.error(
                        request,
                        f'No container with label "{form.fields["label"].value}" found',
                    )
                    return HttpResponseRedirect(".")
                return HttpResponseRedirect(container.get_absolute_url())

            messages.error(request, "Invalid form")
            return HttpResponseRedirect(".")


class ContainerQueryPage(BasePage):
    label_form = ContainerQueryForm()

    class Meta:
        title = "Container Query"
