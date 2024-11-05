# Create your views here.
from iommi import Page, html


class BasePage(Page):
    title = html.h1("HomeBin")


class IndexPage(BasePage):
    content = html.p("Welcome to HomeBin!")


item_label_class = {"fw-bold": True, "text-muted": True}
item_row_class = {"list-group-item": True}


def item_row(label, value):
    return html.li(
        html.span(f"{label}: ", attrs__class=item_label_class),
        value,
        attrs__class=item_row_class,
    )
