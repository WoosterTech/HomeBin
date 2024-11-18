# Create your views here.
import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django_tables2 import SingleTableView
from easy_thumbnails.files import get_thumbnailer
from iommi import html
from iommi.path import register_path_decoding

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


def breadcrumbs_link(location, **kwargs):
    logger.warning("this is something")
    breadcrumbs = location.breadcrumbs()
    a_tag_list = [
        html.a(
            crumb.name, attrs__href=reverse("location-detail", kwargs={"pk": crumb.pk})
        )
        for crumb in breadcrumbs
    ]
    return html.div(*a_tag_list)


class LocationDetailPage(BasePage):
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
    # TODO: add breadcrumbs
    parents = breadcrumbs_link
    table_title = html.h3("Related Containers")
    related_containers = ContainersTable(
        rows=lambda location, **_: location.containers.all(),
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
    primary_image = html.div(
        html.img(
            attrs__src=lambda container, **_: (
                get_thumbnailer(container.primary_image)["medium"].url
                if container.primary_image
                else None
            ),
            attrs__alt=lambda container, **_: container.label,
        ),
    )
    container = html.div(
        html.ul(
            item_row(
                "Description", lambda container, **_: container.container_description
            ),
            item_row("Serial Number", lambda container, **_: container.simple_contents),
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
