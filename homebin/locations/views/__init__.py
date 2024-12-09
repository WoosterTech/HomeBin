from .all_views import (
    ContainerQueryPage,
    breadcrumb_test,
)
from .container_views import ContainerDetailPage
from .location_views import LocationDetailPage

__all__ = [
    "ContainerDetailPage",
    "ContainerQueryPage",
    "LocationDetailPage",
    "breadcrumb_test",
    "container_create",
]
