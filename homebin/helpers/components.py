from iommi import Fragment, Menu, html
from iommi.declarative.namespace import Namespace
from iommi.fragment import Fragment
from iommi.refinable import EvaluatedRefinable, RefinableMembers
from iommi.shortcut import with_defaults


class CardBody(Fragment):
    @with_defaults(
        attrs__class="card-body",
        tag="div",
    )
    def __init__(self, text=None, **kwargs):
        super().__init__(text, **kwargs)


class Card(Fragment):
    title_model_field_name: Namespace = EvaluatedRefinable()

    @with_defaults(
        attrs__class="card",
        tag="div",
    )
    def __init__(self, body_text: str, **kwargs):
        super().__init__(**kwargs)


class NavMenu(Menu):
    @with_defaults(
        attrs__class="navbar navbar-expand-md",
        tag="ul",
    )
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
