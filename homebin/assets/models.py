from django.db import models
from django_rubble.models.history_models import HistoryModel
from django_rubble.models.number_models import NaturalKeyModel


# Create your models here.
class Asset(HistoryModel, NaturalKeyModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    serial_number = models.CharField(max_length=100)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    warranty = models.DateField()
    warranty_provider = models.CharField(max_length=100)
    warranty_phone = models.CharField(max_length=20)
    warranty_email = models.EmailField()
    warranty_notes = models.TextField()
    asset_tag = models.CharField(max_length=100)
    notes = models.TextField()
    natural_key_fields = ["name", "serial_number"]

    def __str__(self):
        return self.name
