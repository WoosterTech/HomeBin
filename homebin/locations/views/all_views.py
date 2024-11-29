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

from homebin.helpers.views import (
    BasePage,
    admin_button_class,
    item_label_class,
)
from homebin.locations.models import Container, Location
from homebin.locations.tables import (
    ContainerTable,
    LocationTable,
)

if TYPE_CHECKING:
    from django.http import HttpRequest

logger = logging.getLogger(__name__)

register_path_decoding(container_label=Container.label, location_pk=Location)

MAX_CONTENT_LINES = 5


def get_container_primary_thumbnail(
    request: "HttpRequest", container: "Container | None", **_
):
    if container.primary_thumbnail is None:
        logger.info("No primary image for %s", container)
        return None
    logger.info(
        "Primary image for %s is %s", container.label, container.primary_thumbnail
    )
    return html.img(
        attrs__src=lambda container, **_: container.primary_thumbnail["medium"].url,
        attrs__alt=lambda container, **_: container.label,
        attrs__loading="lazy",
        attrs={"width": "200", "height": "200"},
    ).bind(request=request)


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
