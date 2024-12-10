from easy_thumbnails.files import get_thumbnailer
from iommi import Column, html

from homebin.helpers.views import BaseAction, BaseTable, project_thumbnail_aliases

alias = project_thumbnail_aliases.THUMBNAIL


class AttachmentImageTable(BaseTable):
    card = Column(
        cell__value=lambda request, row, **_: html.div(
            html.a(
                html.img(
                    attrs__src=get_thumbnailer(row.file)[alias.alias].url,
                    attrs__class={"img-thumbnail": True, "img-fluid": True},
                    attrs__loading="lazy",
                    attrs={"width": alias.width, "height": alias.height},
                ),
                attrs={
                    "href": (row.file.url),
                    "data-lightbox": "primary-thumbnail",
                    "data-alt": row.name,
                },
            ),
            attrs__style__display="inline-block",
        ).bind(request=request),
    )

    class Meta:
        tag = "div"
        header__include = False
        title = "Images"
        actions = BaseAction(
            display_name="Add",
        )
