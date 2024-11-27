import logging
from typing import TYPE_CHECKING

from django.utils.html import format_html
from django.utils.translation import gettext_lazy as __
from iommi import Fragment, html

if TYPE_CHECKING:
    from django.http import HttpRequest, QueryDict

    from homebin.locations.models import Container

logger = logging.getLogger(__name__)

MAX_CONTENT_LINES = 5


# TODO: do this with htmx
def collapsible_widget(
    lines: list[str],
    params: "dict | QueryDict",
    *,
    expand_param: str = "expand_lines",
    **_,
) -> "list[str | Fragment]":
    """Add a button to expand or collapse the lines.

    If the lines are longer than MAX_CONTENT_LINES, the lines will be truncated and a
    button will be added to expand the lines.

    Args:
        lines: The lines to display.
        params: The query parameters to modify.
        expand_param: The query parameter to modify.

    Returns:
        The lines optionally with a button to expand or collapse.
    """
    assert params._mutable, "params must be mutable"  # noqa: SLF001
    expand_lines = params.get(expand_param, "false").lower() == "true"
    button_label = None
    logger.debug("number of lines: %s", len(lines))
    if (not expand_lines) and (len(lines) > MAX_CONTENT_LINES):
        params.__setitem__(expand_param, value=True)
        button_label = __("expand")
        lines = lines[: MAX_CONTENT_LINES - 1]
    if expand_lines and len(lines) > MAX_CONTENT_LINES:
        params.__setitem__(expand_param, value=False)
        button_label = __("collapse")
    if button_label:
        lines.append(
            html.a(
                button_label.title(),
                attrs__href=f"?{params.urlencode()}",
                attrs__class={"link-secondary": True},
                attrs__role="button",
            )
        )

    return lines


def linebreaks(request: "HttpRequest", container: "Container", **_):
    content_lines = container.simple_contents.split("\n")
    lines = [format_html("{}<br>", line) for line in content_lines]
    logger.debug("lines w/ breaks: %s", lines)

    lines = collapsible_widget(lines, request.GET.copy())

    return html.div(*lines).bind(request=request)
