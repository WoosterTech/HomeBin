from django.contrib import admin

from homebin.locations.models import Container, Location

# Register your models here.
admin.site.register(Location)


class ContainerAttachmentInline(admin.TabularInline):
    model = Container.attachments.through
    extra = 1


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ["label", "container_description", "simple_contents", "location"]
    search_fields = ["label", "container_description", "simple_contents"]
    inlines = [ContainerAttachmentInline]
