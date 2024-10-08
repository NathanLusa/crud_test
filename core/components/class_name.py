# could be renamed to something general if there's more to add
from typing import Dict, List, Literal, Union

from pydantic import Field
from typing_extensions import Annotated, TypeAliasType

# ClassName = TypeAliasType('ClassName', Union[str, List['ClassName'], Dict[str, Union[bool, None]], None])
ClassName = TypeAliasType('ClassName', str)
ClassNameField = Annotated[ClassName, Field(serialization_alias='class_name')]

NamedStyle = TypeAliasType('NamedStyle', Union[Literal['primary', 'secondary', 'warning'], None])
NamedStyleField = Annotated[NamedStyle, Field(serialization_alias='named_style')]
