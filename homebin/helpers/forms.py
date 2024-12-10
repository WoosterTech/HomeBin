import logging
from dataclasses import dataclass

from iommi import Form

logger = logging.getLogger(__name__)


@dataclass
class CRUDForms:
    create: Form
    edit: Form
    delete: Form


class BaseForm(Form):
    @classmethod
    def crud_form_factory(cls):
        form_model = cls.model
        logger.debug("form_model: %s", form_model)
        create_form = cls.create()
        edit_form = cls.edit(
            instance=lambda **kwargs: form_model.objects.get(**kwargs),
        )
        delete_form = cls.delete(
            instance=lambda **kwargs: form_model.objects.get(**kwargs),
        )
        return CRUDForms(create=create_form, edit=edit_form, delete=delete_form)
