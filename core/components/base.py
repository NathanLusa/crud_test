import typing as _t

from pydantic import BaseModel


class BaseComponent(BaseModel):
    title: str
    render: bool = True
    visible: bool = True