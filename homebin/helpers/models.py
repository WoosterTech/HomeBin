from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_rubble.models.number_models import NaturalKeyModel, NaturalKeyModelManager


class ItemBaseManager(NaturalKeyModelManager):
    def admin_changelist_url(self):
        return reverse(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist"  # noqa: SLF001
        )


# Create your models here.
class ItemBaseModel(NaturalKeyModel):
    """Model that includes a `get_absolute_url` method that uses the model name and
    a `lookup_field` attribute.

    The `get_absolute_url` method uses the `lookup_field` attribute to create a URL
    named `<model_name>-detail` with the lookup field as a keyword argument."""

    lookup_field: str = "pk"

    objects = ItemBaseManager()

    class Meta:
        abstract = True

    def get_absolute_url(self):
        lookup_kwarg = {self.lookup_field: getattr(self, self.lookup_field)}
        return reverse(f"{self.model_name()}-detail", kwargs=lookup_kwarg)

    def get_admin_change_url(self):
        return reverse(
            f"admin:{self._meta.app_label}_{self._meta.model_name}_change",
            args=[self.pk],
        )

    def get_admin_changelist_url(self):
        return reverse(
            f"admin:{self._meta.app_label}_{self._meta.model_name}_changelist"
        )


class ActiveManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)


class ActiveModel(models.Model):
    """Model that includes an `is_active` field and an `active` manager that filters
    for active instances."""

    is_active = models.BooleanField(_("Active"), default=True)

    active = ActiveManager()

    class Meta:
        abstract = True
