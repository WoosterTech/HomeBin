import admin_thumbnails
from adminsortable2.admin import SortableGenericInlineAdminMixin
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from homebin.attachments.models import GenericAttachment

# Register your models here.


@admin.register(GenericAttachment)
class GenericAttachmentAdmin(admin.ModelAdmin):
    list_display = ["name", "attachment_type", "uploaded_at", "sort_rank"]


@admin_thumbnails.thumbnail("file")
class GenericAttachmentInline(SortableGenericInlineAdminMixin, GenericTabularInline):
    model = GenericAttachment
    extra = 1
