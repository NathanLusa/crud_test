from pydantic import BaseModel
from typing import Type, TypedDict


class BaseUI(BaseModel):
    pass


class TemplateSchemaDict(TypedDict):
    template: str
    schema: Type[BaseModel]
