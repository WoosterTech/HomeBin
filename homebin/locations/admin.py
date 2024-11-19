import admin_thumbnails
from adminsortable2.admin import (
    SortableAdminBase,
)
from django.contrib import admin

from homebin.attachments.admin import GenericAttachmentInline
from homebin.locations.models import Container, Location


# Register your models here.
class ContainerInline(admin.TabularInline):
    model = Container
    extra = 0


class SubLocationInline(admin.TabularInline):
    model = Location
    extra = 0


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = [ContainerInline]


@admin.register(Container)
@admin_thumbnails.thumbnail("primary_image")
class ContainerAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = [
        "label",
        "primary_image_thumbnail",
        "container_description",
        "simple_contents",
        "location",
    ]
    search_fields = ["label", "container_description", "simple_contents"]
    inlines = [GenericAttachmentInline]
