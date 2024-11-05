import logging

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django_rubble.models.history_models import HistoryModel
from easy_thumbnails.files import get_thumbnailer

from homebin.attachments.models import GenericAttachment
from homebin.helpers.models import ItemBaseModel

logger = logging.getLogger(__name__)


# Create your models here.
class Manufacturer(ItemBaseModel):
    name = models.CharField(max_length=100, unique=True)
    natural_key_fields = ["name"]
    slug = AutoSlugField(populate_from="name")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("manufacturer-detail", kwargs={"manufacturer_slug": self.slug})


class Asset(ItemBaseModel, HistoryModel):
    name = models.CharField(max_length=100)
    make = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, default=1)
    model = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    warranty = models.DateField(blank=True, null=True)
    warranty_provider = models.CharField(max_length=100, blank=True)
    warranty_phone = models.CharField(max_length=20, blank=True)
    warranty_email = models.EmailField(blank=True)
    warranty_notes = models.TextField(blank=True)
    asset_tag = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    natural_key_fields = ["name", "serial_number"]
    attachments = GenericRelation(GenericAttachment, related_query_name="asset")

    @property
    def primary_image(self):
        attachment = self.attachments.filter(attachment_type="image").first()
        logger.info("%s primary_image: %s", str(self), attachment)
        return attachment.file if attachment is not None else None

    @property
    def primary_thumbnail(self):
        primary_image = self.primary_image
        if primary_image is not None:
            return get_thumbnailer(primary_image)
        return None

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("asset-detail", kwargs={"asset_pk": self.pk})
