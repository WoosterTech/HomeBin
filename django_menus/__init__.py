from django.views import View
from pydantic import BaseModel


class ProjectApp(BaseModel):
    name: str
    models: list[tuple[str, type[View]]] = []
