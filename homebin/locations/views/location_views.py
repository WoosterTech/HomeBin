import logging
from typing import TYPE_CHECKING

from django.http import HttpRequest
from django.urls import reverse
from iommi import html

from homebin.assets.tables import AssetTable
from homebin.helpers.views import BasePage
from homebin.locations.models import Location
from homebin.locations.tables import ContainersTable, LocationsTable

if TYPE_CHECKING:
    from django.http import HttpRequest

logger = logging.getLogger(__name__)


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
