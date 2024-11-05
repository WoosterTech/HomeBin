from django.urls import reverse
from django_rubble.models.number_models import NaturalKeyModel


# Create your models here.
class ItemBaseModel(NaturalKeyModel):
    """Model that includes a `get_absolute_url` method that uses the model name and
    a `lookup_field` attribute.

    The `get_absolute_url` method uses the `lookup_field` attribute to create a URL
    named `<model_name>-detail` with the lookup field as a keyword argument."""

    lookup_field: str = "pk"

    class Meta:
        abstract = True

    def get_absolute_url(self):
        lookup_kwarg = {self.lookup_field: getattr(self, self.lookup_field)}
        return reverse(f"{self.model_name()}-detail", kwargs=lookup_kwarg)

    def model_name(self):
        return self._meta.model_name
