from pydantic import BaseModel
from typing import List

from core.components import DataAttr
from .enums import FormatType


class OptionType(BaseModel):
    desc: str
    value: str


class ComponentType:
    type: str
    required: bool = False
    properties: any


def get_type(item: str, schema: dict) -> ComponentType:
    properties: dict = None

    if 'properties' in schema:
        properties = schema['properties'][item]
        _props = properties['default']
    else:
        _props = schema
        
    _type = _props['type'] if 'type' in _props else ''

    # print(item, properties if properties else _props)

    if ('render' in _props) and (not _props['render']):
        return None

    component = ComponentType()
    component.type = _type
    component.required = _props['required'] if 'required' in _props else False
    component.properties = _props

    return component

def format(value, arg):
    # print(value, arg, type(value))
    return value

    match arg:
        case FormatType.CURRENCY | FormatType.CURRENCY.value:
            return "R$ {:,.2f}".format(value if value else 0)
        case FormatType.DATE | FormatType.DATE.value:
            return value.strftime('%d/%m/%Y')
        case FormatType.DATETIME | FormatType.DATETIME.value:
            return value.strftime('%d/%m/%Y %H:%M:%S')
        case FormatType.DECIMAL | FormatType.DECIMAL.value:
            return "R$ {:,.2f}".format(value if value else 0)
        case FormatType.TIME | FormatType.TIME.value:
            return value.strftime('%H:%M:%S')
        case FormatType.INTEGER | FormatType.INTEGER.value:
            return value if value else 0
        case FormatType.PERCENT | FormatType.PERCENT.value:
            return "{:,.2f} %".format(value if value else 0)

    return value

def get_data_attribute(data_list: List[DataAttr], name: str) -> List[str]:
    return filter(lambda x: x.name == name, data_list)

def carousel_images(data_list: List[DataAttr]) -> List[str]:
    images = next(get_data_attribute(data_list, 'images'), None)
    return images.value.split(';') if images else []

processors = [
    carousel_images,
    format, 
    get_data_attribute,
    get_type, 
]