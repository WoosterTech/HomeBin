import admin_thumbnails
from adminsortable2.admin import SortableAdminBase
from django.contrib import admin

from homebin.assets.models import Asset, Manufacturer
from homebin.attachments.admin import GenericAttachmentInline


# Register your models here.
# @admin_thumbnails.thumbnail("primary_image")
class AssetInline(admin.TabularInline):
    model = Asset
    extra = 0
    fields = ["name", "model"]


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [AssetInline]


@admin.register(Asset)
@admin_thumbnails.thumbnail("primary_image")
class AssetAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["name", "make", "model", "primary_image_thumbnail"]
    inlines = [GenericAttachmentInline]
