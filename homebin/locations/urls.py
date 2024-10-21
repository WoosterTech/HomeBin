from django.urls import path

from homebin.locations.views import (
    ContainerListView,
    LocationListView,
    container_detail,
    location_detail,
)

app_name = "locations"
urlpatterns = [
    path("container/<str:label>/", container_detail, name="container_detail"),
    path("container/", ContainerListView.as_view(), name="container_list"),
    path("location/<int:pk>/", location_detail, name="location_detail"),
    path("location/", LocationListView.as_view(), name="location_list"),
]
