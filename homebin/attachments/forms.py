from iommi import Field

from homebin.assets.models import Asset
from homebin.attachments.models import GenericAttachment
from homebin.helpers.forms import BaseForm


class AttachmentForm(BaseForm):
    asset = Field.choice(choices=Asset.objects.all())
    file = Field.file()
    attachment_type = Field.choice(choices=GenericAttachment.TYPE_CHOICES)

    class Meta:
        auto__model = GenericAttachment


attachment_forms = AttachmentForm.crud_form_factory()
