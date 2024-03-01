from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.models import BaseModel
from shortuuid.django_fields import ShortUUIDField


# Create your models here.
class Location(BaseModel):
    parent_location = models.ForeignKey(
        "self",
        verbose_name=_("Parent"),
        on_delete=models.SET_NULL,
        null=True,
    )
    id = ShortUUIDField(length=10, primary_key=True)
