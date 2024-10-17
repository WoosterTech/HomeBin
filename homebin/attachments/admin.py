import admin_thumbnails
from django.contrib import admin

from homebin.attachments.models import Attachment


# Register your models here.
@admin.register(Attachment)
@admin_thumbnails.thumbnail("attachment")
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "attachment_thumbnail"]
