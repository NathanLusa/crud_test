import typing as _t

from pydantic import BaseModel


class SelectOption(BaseModel):
    value: str
    label: str
    type: _t.Literal['SelectOption'] = 'SelectOption'


class DataAttr(BaseModel):
    name: str
    value: str


