from typing import Type, Optional, Callable, Sequence, Union
from enum import Enum

from fastcrud import EndpointCreator
from fastcrud.crud.fast_crud import FastCRUD
from fastcrud import FilterConfig
from fastcrud.types import (
    CreateSchemaType,
    DeleteSchemaType,
    ModelType,
    UpdateSchemaType,
)


class BaseEndpointCreator(EndpointCreator):

    def __init__(
        self,
        session: Callable,
        model: ModelType,
        create_schema: Type[CreateSchemaType],
        update_schema: Type[UpdateSchemaType],
        crud: Optional[FastCRUD] = None,
        include_in_schema: bool = True,
        delete_schema: Optional[Type[DeleteSchemaType]] = None,
        path: str = "",
        tags: Optional[list[Union[str, Enum]]] = None,
        is_deleted_column: str = "is_deleted",
        deleted_at_column: str = "deleted_at",
        updated_at_column: str = "updated_at",
        endpoint_names: Optional[dict[str, str]] = None,
        filter_config: Optional[Union[FilterConfig, dict]] = None,
    ) -> None:
        self._endpoint_names = endpoint_names or {
            "create": "",
            "read": "",
            "update": "",
            "delete": "",
            "read_multi": "",
            "read_paginated": "paginate",
        }

        super().__init__(
            session,
            model,
            create_schema,
            update_schema,
            crud,
            include_in_schema,
            delete_schema,
            path,
            tags,
            is_deleted_column,
            deleted_at_column,
            updated_at_column,
            self._endpoint_names,
            filter_config,
        )

    def _custom_route(self):
        async def custom_endpoint():
            # Custom endpoint logic
            return {"message": "Custom route"}

        return custom_endpoint

    def add_routes_to_router(
        self,
        create_deps: Sequence[Callable] = [],
        read_deps: Sequence[Callable] = [],
        read_multi_deps: Sequence[Callable] = [],
        read_paginated_deps: Sequence[Callable] = [],
        update_deps: Sequence[Callable] = [],
        delete_deps: Sequence[Callable] = [],
        db_delete_deps: Sequence[Callable] = [],
        included_methods: Optional[Sequence[str]] = None,
        deleted_methods: Optional[Sequence[str]] = None,
    ):
        self._deleted_methods = deleted_methods or []
        self._deleted_methods.append('read_paginated')
        super().add_routes_to_router(
            create_deps,
            read_deps,
            read_multi_deps,
            read_paginated_deps,
            update_deps,
            delete_deps,
            db_delete_deps,
            included_methods,
            self._deleted_methods,
        )

        # Now, add custom routes
        self.router.add_api_route(
            path="/custom",
            endpoint=self._custom_route(),
            methods=["GET"],
            tags=self.tags,
            # Other parameters as needed
        )


class BaseAPIEndpointCreator(BaseEndpointCreator):
    pass