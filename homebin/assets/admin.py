import admin_thumbnails
from adminsortable2.admin import SortableAdminBase
from django.contrib import admin
from iommi.admin import Admin

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


def primary_image_thumbnail(row, **kwargs):
    return row.primary_thumbnail["thumbnail"]


class MyAdmin(Admin):
    class Meta:
        apps__assets_asset__include = True
        parts__list_assets_asset__columns = {
            "purchase_price": {"include": False},
            "description": {"include": False},
            "serial_number": {"include": False},
            "purchase_date": {"include": False},
            "warranty": {"include": False},
            "warranty_provider": {"include": False},
            "warranty_phone": {"include": False},
            "warranty_email": {"include": False},
            "warranty_notes": {"include": False},
            "notes": {"include": False},
        }
        parts__list_assets_asset__columns__name__cell = {
            "url": lambda row, **_: row.get_absolute_url()
        }
        parts__list_assets_asset__columns__primary_image__cell = {
            "value": primary_image_thumbnail,
            "template": "table_thumbnail.html",
        }
