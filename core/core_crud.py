from typing import Optional, Callable, Any, List

from fastcrud import FastCRUD
from fastcrud.types import ModelType
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import BaseLookupSchema
from core.types import TemplateSchemaDict

class CoreCRUD(FastCRUD):
    def __init__(
        self,
        model: type[ModelType],
        is_deleted_column: str = "is_deleted",
        deleted_at_column: str = "deleted_at",
        updated_at_column: str = "updated_at",
    ) -> None:
        super().__init__(
            model,
            is_deleted_column,
            deleted_at_column,
            updated_at_column,
        )


class ApiCRUD(CoreCRUD):
    def __init__(
        self,
        model: type[ModelType],
        is_deleted_column: str = "is_deleted",
        deleted_at_column: str = "deleted_at",
        updated_at_column: str = "updated_at",

        lookup_filter: Optional[Callable] = None,
        lookup_solver: Optional[Callable] = None,
    ) -> None:
        super().__init__(
            model,
            is_deleted_column,
            deleted_at_column,
            updated_at_column,
        )

        self.lookup_filter = lookup_filter
        self.lookup_solver = lookup_solver


    async def _lookup(self, db: AsyncSession, find: str = '', **kwargs: Any) -> List[BaseLookupSchema]:
        _filter = {}
        if self.lookup_filter: 
            _filter = self.lookup_filter(find)

        query = await self.get_multi(db, **_filter)

        return self.lookup_solver(query)


class FormCRUD(CoreCRUD):
    def __init__(
        self,
        model: type[ModelType],
        is_deleted_column: str = "is_deleted",
        deleted_at_column: str = "deleted_at",
        updated_at_column: str = "updated_at",

        form: Optional[TemplateSchemaDict] = None,
        lista: Optional[TemplateSchemaDict] = None,

        get_schema_component: Optional[Callable] = None,
        get_schema_data_list: Optional[Callable] = None,
        get_schema_value: Optional[Callable] = None,
    ) -> None:
        super().__init__(
            model,
            is_deleted_column,
            deleted_at_column,
            updated_at_column,
        )

        self.form = form
        self.lista = lista

        self.get_schema_component = get_schema_component
        self.get_schema_data_list = get_schema_data_list
        self.get_schema_value = get_schema_value



class FormAPICRUD(ApiCRUD, FormCRUD):
    pass