import logging

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_rubble.models.history_models import HistoryModel
from django_rubble.models.number_models import NaturalKeyModel
from django_rubble.utils.strings import Alphabet, truncate_string, uuid_ish
from easy_thumbnails.files import get_thumbnailer

logger = logging.getLogger(__name__)


# Create your models here.
class Location(HistoryModel, NaturalKeyModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent_location = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    natural_key_fields = ["name"]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def get_absolute_url(self):
        logger.debug("get_absolute_url: %s", self.pk)
        return reverse("location-detail", args=[self.pk])

    def breadcrumbs(self) -> list["Location"]:
        breadcrumbs = [self] + (
            self.parent_location.breadcrumbs() if self.parent_location else []
        )
        logger.debug("breadcrumbs: %s", breadcrumbs)
        return breadcrumbs


def default_container_label():
    """A simple way to generate a unique label for containers."""
    # use uuid_ish to generate a 5 character label
    # confirm that it is unique in Containers
    # return the label
    alphabet = Alphabet.UNAMBIGUOUS_ALPHANUMERIC_UPPER
    label_length = 5
    label = uuid_ish(label_length, alphabet=alphabet)
    while Container.objects.filter(label=label).exists():
        label = uuid_ish(label_length, alphabet=alphabet)
    return label


class Container(HistoryModel, NaturalKeyModel):
    label = models.CharField(
        max_length=25, unique=True, default=default_container_label
    )
    container_description = models.CharField(
        _("description of container"),
        help_text=_("e.g. 'black w/ yellow lid'"),
        max_length=100,
    )
    simple_contents = models.TextField(_("simple description of contents"), blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name="containers",
        null=True,
        blank=True,
    )
    natural_key_fields = ["label"]

    attachments_generic = GenericRelation(
        "attachments.GenericAttachment", related_query_name="containers"
    )

    @property
    def primary_image(self):
        attachment = self.attachments_generic.filter(attachment_type="image").first()
        logger.info("%s primary_image: %s", str(self), attachment)
        return attachment.file if attachment is not None else None

    @property
    def primary_thumbnail(self):
        primary_image = self.primary_image
        if primary_image is not None:
            return get_thumbnailer(primary_image)
        return None

    def __str__(self):
        return (
            f"{self.label} | {truncate_string(self.container_description, num_char=20)}"
        )

    def get_absolute_url(self):
        return reverse("container-detail", args=[self.label])
