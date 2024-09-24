import typing as _t

from pydantic import BaseModel

from .attribute import DataAttr, SelectOption
from .base import BaseComponent
from core.enums import FormatType

TableAction = _t.Literal['edit', 'delete']

class TableColumn(BaseModel):
    name: str
    format: _t.Optional[FormatType] = None
    data_list: _t.Optional[_t.List[DataAttr]] = None
    action_list: _t.Optional[_t.List[TableAction]] = None
    custom_action_list: _t.Optional[_t.List[str]] = None

    type: _t.Literal['TableColumn'] = 'TableColumn'


class Table(BaseComponent):
    title: '_t.List[AnyComponent]'
    name: _t.Optional[str] = ''
    columns: _t.List[TableColumn]
    data_list: _t.Optional[_t.List[DataAttr]]

    type: _t.Literal['Table'] = 'Table'
