import typing as _t
import typing_extensions as _te
import pydantic as _p

from pydantic import BaseModel

from core.enums import FormatType
from .attribute import *
from . import class_name as _class_name
from .components import (
    Input,
    Select,
    Switch,
    Lookup,
    Carousel,
)
from .tables import Table, TableColumn

__all__ = (
    # first we include all components from this file
    'Text',
    # 'Paragraph',
    # 'PageTitle',
    'Div',
    'Form',
    # 'Page',
    # 'Heading',
    # 'Markdown',
    # 'Code',
    # 'Json',
    'Button',
    'Link',
    # 'LinkList',
    # 'Navbar',
    'Modal',
    # 'ServerLoad',
    # 'Image',
    # 'Iframe',
    # 'FireEvent',
    # 'Error',
    # 'Spinner',
    # 'Toast',
    # 'Custom',
    # # then we include components from other files
    'Table',
    # 'Pagination',
    # 'Display',
    # 'Details',
    # 'Form',
    # 'FormField',
    # 'ModelForm',
    # 'Footer',
    # then `AnyComponent` itself
    'AnyComponent',
    # then the other form field types which are included in `AnyComponent` via the `FormField` union
    'Input',
    'Select',
    'Switch',
    'Lookup',
    'Carousel',
    # 'FormFieldBoolean',
    # 'FormFieldFile',
    # 'FormFieldInput',
    # 'FormFieldSelect',
    # 'FormFieldSelectSearch',
)

class Button(BaseModel, extra='forbid'):
    name: str
    label: str
    # on_click: _t.Union[events.AnyEvent, None] = None
    html_type: _t.Union[_t.Literal['button', 'reset', 'submit'], None] = None
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Button'] = 'Button'


class Div(BaseModel):
    components: '_t.List[AnyComponent]'
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Div'] = 'Div'


FormMethods = _t.Literal['GET', 'POST', 'PUT', 'DELETE']
FormPostType = _t.Literal['BODY', 'JSON']

class Form(BaseModel):
    action: _t.Optional[str] = None
    method: _t.Optional[FormMethods] = None
    components: '_t.List[AnyComponent]'
    class_name: _class_name.ClassNameField = None
    post_type: _t.Optional[FormPostType] = 'BODY'
    name: _t.Optional[str] = ''
    type: _t.Literal['Form'] = 'Form'


class Link(BaseModel, extra='forbid'):
    href: str
    components: '_t.List[AnyComponent]'
    class_name: _class_name.ClassNameField = None
    data_list: _t.Optional[_t.List[DataAttr]] = None
    type: _t.Literal['Link'] = 'Link'


class Modal(BaseModel):
    name: str
    title: str
    button_title: str
    show_footer: bool = True
    body: '_t.Optional[_t.List[AnyComponent]]' = None
    form_url_body: str = None
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Modal'] = 'Modal'

TextType = _t.Literal['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

class Text(BaseModel, extra='forbid'):
    text: str
    html_type: _t.Optional[TextType] = ''
    class_name: _class_name.ClassNameField = None
    type: _t.Literal['Text'] = 'Text'


AnyComponent = _te.Annotated[
    _t.Union[
        Text,
        # Paragraph,
        # PageTitle,
        Div,
        Form,
        # Page,
        # Heading,
        # Markdown,
        # Code,
        # Json,
        Button,
        Link,
        # LinkList,
        # Navbar,
        # Footer,
        Modal,
        # ServerLoad,
        # Image,
        # Iframe,
        # Video,
        # FireEvent,
        # Error,
        # Spinner,
        # Custom,
        Table,
        # Pagination,
        # Display,
        # Details,
        # Form,
        # FormField,
        # ModelForm,
        # Toast,
        Input,
        Select,
        Switch,
        Lookup,
        Carousel,
    ],
    _p.Field(discriminator='type'),
]
