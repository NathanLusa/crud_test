import typing as _t

from pydantic import BaseModel

from .attribute import DataAttr, SelectOption
from .base import BaseComponent

InputHtmlType = _t.Literal['text', 'date', 'time', 'email', 'number', 'password', 'hidden']

class Input(BaseComponent):
    html_type: InputHtmlType = 'text'
    class_name: str = ''
    name: str
    value: str
    placeholder: str
    required: bool
    type: _t.Literal['Input'] = 'Input'


class Select(BaseComponent):
    name: str
    options: _t.List[SelectOption]
    value: str = ''
    required: bool
    type: _t.Literal['Select'] = 'Select'


class Switch(BaseComponent):
    name: str
    value: str = ''
    required: bool
    type: _t.Literal['Switch'] = 'Switch'


class Lookup(BaseComponent):
    name: str
    required: bool
    value: str = ''
    data_list: _t.Optional[_t.List[DataAttr]]
    type: _t.Literal['Lookup'] = 'Lookup'


class Carousel(BaseComponent):
    name: str
    class_name: str = ''
    data_list: _t.Optional[_t.List[DataAttr]]
    type: _t.Literal['Carousel'] = 'Carousel'
