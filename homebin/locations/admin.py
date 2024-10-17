import admin_thumbnails
from adminsortable2.admin import SortableAdminBase, SortableTabularInline
from django.contrib import admin

from homebin.locations.models import Container, Location

# Register your models here.
admin.site.register(Location)


@admin_thumbnails.thumbnail("attachment_image")
class ContainerAttachmentInline(SortableTabularInline):
    model = Container.attachments.through
    extra = 1


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
    inlines = [ContainerAttachmentInline]
