# ruff: noqa: E501
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from homebin.assets.admin import MyAdmin
from homebin.assets.tables import ManufacturerTable
from homebin.assets.views import (
    AssetAttachmentForm,
    ManufacturerDetailPage,
    manufacturer_create_form,
    manufacturer_delete_form,
    manufacturer_edit_form,
)
from homebin.attachments.forms import attachment_forms
from homebin.helpers.views import IndexPage
from homebin.locations.tables import ContainerCardTable, LocationsTable
from homebin.locations.views import (
    ContainerDetailPage,
    ContainerQueryPage,
    LocationDetailPage,
    breadcrumb_test,
)
from homebin.locations.views.container_views import container_forms
from homebin.locations.views.location_views import location_forms

# fmt: off
urlpatterns = [
    path("", IndexPage().as_view(), name="home"),
    path( "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("homebin.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("containers/", ContainerCardTable().as_view(), name="container-list"),
    path("containers/create/", container_forms.create.as_view(), name="container-create"),
    path("containers/find/", ContainerQueryPage().as_view(), name="container-scan"),
    path("containers/<container_label>/edit/", container_forms.edit.as_view(), name="container-edit"),
    path("containers/<container_label>/delete/", container_forms.delete.as_view(), name="container-delete"),
    path("containers/<container_label>/attachments/add/", attachment_forms.create.as_view(), name="container-add-attachment"),
    path("containers/<container_label>/", ContainerDetailPage().as_view(), name="container-detail"),
    path("locations/", LocationsTable().as_view(), name="location-list"),
    path("locations/create/", location_forms.create.as_view(), name="location-create"),
    path("locations/<location_pk>/edit/", location_forms.edit.as_view(), name="location-edit"),
    path("locations/<location_pk>/delete/", location_forms.delete.as_view(), name="location-delete"),
    path("locations/<location_pk>/", LocationDetailPage().as_view(),name="location-detail"),
    path("assets/", include("homebin.assets.urls")),
    path("manufacturers/", ManufacturerTable().as_view(), name="manufacturer-list"),
    path("manufacturers/create/", manufacturer_create_form.as_view(), name="manufacturer-create"),
    path("manufacturers/<manufacturer_slug>/delete/", manufacturer_delete_form.as_view(), name="manufacturer-delete"),
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

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls)), *urlpatterns]
# fmt: on
