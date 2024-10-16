from django.db import models
from django.utils.translation import gettext_lazy as _
from django_rubble.models.history_models import HistoryModel
from django_rubble.models.number_models import NaturalKeyModel
from django_rubble.utils.strings import Alphabet, truncate_string, uuid_ish


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
        _("description of container; e.g. 'black w/ yellow lid'"), max_length=100
    )
    simple_contents = models.TextField(_("simple description of contents"), blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name="containers",
        null=True,
        blank=True,
    )
    attachments = models.ManyToManyField(
        "attachments.Attachment",
        through="ContainerAttachment",
    )
    natural_key_fields = ["label"]

    def __str__(self):
        return (
            f"{self.label} | {truncate_string(self.container_description, num_char=20)}"
        )


class ContainerAttachment(models.Model):
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="container_attachments"
    )
    attachment = models.ForeignKey(
        "attachments.Attachment", on_delete=models.CASCADE, related_name="containers"
    )
    description = models.TextField(blank=True)
    natural_key_fields = ["container", "attachment"]
    rank = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["container", "attachment"], name="unique_container_attachment"
            ),
            models.UniqueConstraint(
                fields=["container", "rank"], name="unique_container_rank"
            ),
        ]
        verbose_name = "Container Attachment"
        verbose_name_plural = "Container Attachments"
        ordering = ["container", "attachment"]

    def __str__(self):
        return f"{self.container} - {self.attachment}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.rank = self.container.attachments.count()
        super().save(*args, **kwargs)
