from .all_views import (
    ContainerQueryPage,
    breadcrumb_test,
)
from .container_views import ContainerCreatePage, ContainerDetailPage, ContainerListPage
from .location_views import LocationDetailPage, LocationListPage

__all__ = [
    "ContainerCreatePage",
    "ContainerDetailPage",
    "ContainerListPage",
    "ContainerQueryPage",
    "LocationDetailPage",
    "LocationListPage",
    "breadcrumb_test",
    "container_create",
]
