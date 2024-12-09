# ruff: noqa: E501
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# from iommi import Form
from iommi import Form
from rest_framework.authtoken.views import obtain_auth_token

from homebin.assets.admin import MyAdmin
from homebin.assets.models import Asset, Manufacturer
from homebin.assets.tables import AssetTable, ManufacturerTable
from homebin.assets.views import (
    AssetAttachmentForm,
    AssetDetailPage,
    ManufacturerDetailPage,
    asset_edit_form,
    manufacturer_edit_form,
)
from homebin.helpers.views import IndexPage
from homebin.locations.models import Container, Location
from homebin.locations.tables import ContainerCardTable, LocationsTable
from homebin.locations.views import (
    ContainerDetailPage,
    ContainerQueryPage,
    LocationDetailPage,
    breadcrumb_test,
)
from homebin.locations.views.container_views import container_edit_form
from homebin.locations.views.location_views import location_edit_form

# fmt: off
urlpatterns = [
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("", IndexPage().as_view(), name="home"),
    path( "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("homebin.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    # path("locations/", include("homebin.locations.urls", namespace="locations")),
    path("containers/", ContainerCardTable().as_view(), name="container-list"),
    path("containers/create/", Form.create(auto__model=Container).as_view(), name="container-create"),
    path("containers/find/", ContainerQueryPage().as_view(), name="container-scan"),
    path("containers/<container_label>/edit/", container_edit_form.as_view(), name="container-edit"),
    path("containers/<container_label>/", ContainerDetailPage().as_view(), name="container-detail"),
    path("locations/", LocationsTable().as_view(), name="location-list"),
    path("locations/create/", Form.create(auto__model=Location).as_view(), name="location-create"),
    path("locations/<location_pk>/edit/", location_edit_form.as_view(), name="location-edit"),
    path("locations/<location_pk>/", LocationDetailPage().as_view(),name="location-detail"),
    path("assets/", AssetTable().as_view(), name="asset-list"),
    path("assets/create/", Form.create(auto__model=Asset).as_view(), name="asset-create"),
    path("assets/<asset_pk>/edit/", asset_edit_form.as_view(), name="asset-edit"),
    path("assets/<asset_pk>/", AssetDetailPage().as_view(), name="asset-detail"),
    path("manufacturers/", ManufacturerTable().as_view(), name="manufacturer-list"),
    path("manufacturers/create/", Form.create(auto__model=Manufacturer).as_view(), name="manufacturer-create"),
    path("manufacturers/<manufacturer_slug>/edit/", manufacturer_edit_form.as_view(), name="manufacturer-edit"),
    path("manufacturers/<manufacturer_slug>/", ManufacturerDetailPage().as_view(), name="manufacturer-detail"),
    path("attachments/<attachment_pk>/edit/", AssetAttachmentForm().as_view()),
    path("iommi-admin/", include(MyAdmin.urls())),
    path("locations/<int:pk>/breadcrumbs/", breadcrumb_test),
    path("datawizard/", include("data_wizard.urls")),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("api/auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
# fmt: on
