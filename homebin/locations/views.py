# Create your views here.
from django.http import HttpRequest
from django.shortcuts import render
from django_tables2 import SingleTableView

from homebin.locations.models import Container, Location
from homebin.locations.tables import ContainerTable, LocationTable


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
