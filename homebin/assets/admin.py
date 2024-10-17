from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from homebin.assets.models import Asset, Manufacturer
from homebin.attachments.models import GenericAttachment

# Register your models here.
admin.site.register(Manufacturer)


class GenericAttachmentInline(GenericTabularInline):
    model = GenericAttachment
    extra = 0


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    inlines = [GenericAttachmentInline]
