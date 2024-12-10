import logging
from typing import TYPE_CHECKING

from django.http import HttpRequest
from django.urls import reverse
from iommi import Form, html

from homebin.assets.tables import AssetTable
from homebin.helpers.forms import BaseForm
from homebin.helpers.views import ItemBasePage
from homebin.locations.models import Location
from homebin.locations.tables import ContainerCardTable, LocationsTable

if TYPE_CHECKING:
    from django.http import HttpRequest

logger = logging.getLogger(__name__)


def breadcrumbs_link(request: "HttpRequest", location: Location, **kwargs):
    logger.debug("breadcrumbs_link: %s", location)
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


class LocationDetailPage(ItemBasePage):
    breadcrumbs = html.nav(breadcrumbs_link, attrs__aria_label="breadcrumb", after=-1)

    sub_locations = LocationsTable(
        rows=lambda location, **_: location.location_set.all(),
        columns__parent_location__render_column=False,
        title="Child Locations",
        actions=None,
        query__form__include=False,
        query__advanced__include=False,
        include=lambda location, **_: location.location_set.exists(),
    )

    related_containers = ContainerCardTable(
        rows=lambda location, **_: location.containers.all(),
        title="Containers",
        actions=None,
        query__form__include=False,
        query__advanced__include=False,
        include=lambda location, **_: location.containers.exists(),
    )

    related_assets = AssetTable(
        rows=lambda location, **_: location.asset_set.all(),
        actions=None,
        query__form__include=False,
        title="Assets",
        query__advanced__include=False,
        include=lambda location, **_: location.asset_set.exists(),
    )

    class Meta:
        title = lambda location, **_: location.name  # noqa: E731
        model = Location


location_edit_form = Form.edit(
    auto__model=Location,
    instance=lambda location_pk, **_: Location.objects.get(pk=location_pk),
)


class LocationForm(BaseForm):
    class Meta:
        auto__model = Location


location_forms = LocationForm.crud_form_factory()
