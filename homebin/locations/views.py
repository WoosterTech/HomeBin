# Create your views here.
import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django_tables2 import SingleTableView
from iommi import html
from iommi.path import register_path_decoding

from homebin.assets.tables import AssetTable
from homebin.helpers.views import BasePage, item_label_class, item_row, item_row_class
from homebin.locations.models import Container, Location
from homebin.locations.tables import (
    ContainersTable,
    ContainerTable,
    LocationsTable,
    LocationTable,
)

logger = logging.getLogger(__name__)

register_path_decoding(container_label=Container.label, location_pk=Location)


def primary_thumbnail_or_none(request: HttpRequest, container: "Container | None", **_):
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


def breadcrumbs_link(request: HttpRequest, location: Location, **kwargs):
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
        rows=lambda location, **_: location.containers.all(),
    )

    asset_table_title = html.h3("Related Assets")
    related_assets = AssetTable(
        rows=lambda location, **_: location.asset_set.all(),
    )


class ContainerListPage(BasePage):
    title = html.h1("Container List")
    actions = html.div(
        html.a(
            "New",
            attrs__href=lambda **_: reverse("container-create"),
            attrs__class={"btn": True, "btn-primary": True},
        ),
        html.a(
            "Admin",
            attrs__href=lambda **_: reverse("admin:locations_container_changelist"),
            attrs__class={"btn": True, "btn-secondary": True},
        ),
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


class ContainerDetailPage(BasePage):
    title = html.h1(lambda container, **_: container.label)
    actions = html.div(
        html.a(
            "List",
            attrs__href=lambda **_: reverse("container-list"),
            attrs__class={"btn": True, "btn-primary": True},
        ),
        html.a(
            "Admin",
            attrs__href=lambda **_: reverse("admin:locations_container_changelist"),
            attrs__class={"btn": True, "btn-secondary": True},
        ),
        attrs__class={"btn-group": True},
    )
    primary_image = html.div(primary_thumbnail_or_none, attrs__class={"mt-3": True})
    container = html.div(
        html.ul(
            item_row(
                "Description", lambda container, **_: container.container_description
            ),
            item_row("Contents", lambda container, **_: container.simple_contents),
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


def container_detail(request: HttpRequest, label: str):
    container = Container.objects.get(label=label)
    context = {"object": container}

    return render(request, "locations/container_detail.html", context)


class ContainerListView(SingleTableView):
    model = Container
    table_class = ContainerTable
    template_name = "locations/container_list.html"


def location_detail(request: HttpRequest, pk: int):
    location = Location.objects.get(pk=pk)
    context = {"object": location}

    return render(request, "locations/location_detail.html", context)


class LocationListView(SingleTableView):
    model = Location
    table_class = LocationTable
    template_name = "base_list.html"


def breadcrumb_test(request: HttpRequest, pk: int):
    location = Location.objects.get(pk=pk)
    return HttpResponse(
        f"Breadcrumbs are {[loc.name for loc in location.breadcrumbs()]}"
    )
