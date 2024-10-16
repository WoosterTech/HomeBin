from django.db import models
from django_rubble.models.history_models import HistoryModel
from django_rubble.utils.default_funcs import django_today
from typeid import TypeID


# Create your models here.
def attachment_upload_to(instance: "Attachment", filename: str):
    file_extension = filename.split(".")[-1]
    file_id = TypeID(prefix="att")
    today = django_today()
    year = today.year
    month = str(today.month).zfill(2)
    return f"attachments/{year}/{month}/{file_id}.{file_extension}"


class Attachment(HistoryModel):
    name = models.CharField(max_length=100)
    attachment = models.FileField(upload_to=attachment_upload_to)
    description = models.TextField(blank=True)
    TYPE_CHOICES = {
        ("image", "Image"),
        ("document", "Document"),
        ("audio", "Audio"),
        ("video", "Video"),
    }
    type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, default="image", blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"
