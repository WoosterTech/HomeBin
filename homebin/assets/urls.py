from django.urls import path

from homebin.assets.tables import AssetTable
from homebin.assets.views import (
    AssetDetailPage,
    asset_create_form,
    asset_delete_form,
    asset_edit_form,
)

app_name = "assets"
urlpatterns = [
    path("", AssetTable().as_view(), name="asset-list"),
    path("create/", asset_create_form.as_view(), name="asset-create"),
    path("<asset_pk>/edit/", asset_edit_form.as_view(), name="asset-edit"),
    path("<asset_pk>/delete/", asset_delete_form.as_view(), name="asset-delete"),
    path("<asset_pk>/", AssetDetailPage().as_view(), name="asset-detail"),
]
