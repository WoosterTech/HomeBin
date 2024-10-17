from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django_rubble.models.history_models import HistoryModel
from django_rubble.models.number_models import NaturalKeyModel

from homebin.attachments.models import GenericAttachment


# Create your models here.
class Manufacturer(NaturalKeyModel):
    name = models.CharField(max_length=100)
    natural_key_fields = ["name"]

    def __str__(self):
        return self.name


class Asset(HistoryModel, NaturalKeyModel):
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

    def __str__(self):
        return self.name
