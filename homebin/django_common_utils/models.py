"""Models for common usage."""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from slugify import slugify


# Create your models here.
class BaseModel(models.Model):
    """Base class for all "user-created" models."""
    name = models.CharField(_("name"), max_length=50)
    created_datetime = models.DateTimeField(_("created"), auto_now=False, auto_now_add=True)
    modified_dateteme = models.DateTimeField(_("modified"), auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("created by"),
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("modified by"),
        on_delete=models.CASCADE,
        related_name="%(class)s_modified_by"
    )
    slug = models.SlugField(_("slug"), editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        if self._state.adding:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)