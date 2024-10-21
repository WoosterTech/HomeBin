from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_rubble.utils.default_funcs import django_today
from typeid import TypeID


# Create your models here.
def attachment_upload_to(instance: "GenericAttachment", filename: str):
    file_extension = filename.split(".")[-1]
    file_id = TypeID(prefix="att")
    today = django_today()
    year = today.year
    month = str(today.month).zfill(2)
    return f"attachments/{year}/{month}/{file_id}.{file_extension}"


class GenericAttachment(models.Model):
    file = models.FileField(upload_to=attachment_upload_to)
    name = models.CharField(max_length=100, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    TYPE_CHOICES = [
        ("image", "Image"),
        ("document", "Document"),
        ("audio", "Audio"),
        ("video", "Video"),
    ]
    attachment_type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, default="image"
    )
    sort_rank = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        ordering = ["sort_rank"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.file.name
        super().save(*args, **kwargs)
