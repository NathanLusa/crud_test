from typing import Type, Optional, Callable, Sequence, Union, List, Any
from enum import Enum

from fastapi import Depends, Request
from fastcrud import EndpointCreator
from fastcrud.crud.fast_crud import FastCRUD
from fastcrud import FilterConfig
from fastcrud.types import (
    CreateSchemaType,
    DeleteSchemaType,
    ModelType,
    UpdateSchemaType,
)
from sqlalchemy.ext.asyncio import AsyncSession

import core.json_schema as _j
from core import utils
from core.schemas import BaseLookupSchema
from core.templates import templates



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
        # self.router.add_api_route(
        #     path="/custom",
        #     endpoint=self._custom_route(),
        #     methods=["GET"],
        #     tags=self.tags,
        #     # Other parameters as needed
        # )


class BaseAPIEndpointCreator(BaseEndpointCreator):

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
        super().add_routes_to_router(
            create_deps,
            read_deps,
            read_multi_deps,
            read_paginated_deps,
            update_deps,
            delete_deps,
            db_delete_deps,
            included_methods,
            deleted_methods,
        )


        if self.crud and self.crud.lookup_solver:
            self.add_custom_route(
            # self.router.add_api_route(
                path='/lookup/',
                endpoint=self._lookup(),
                methods=['GET'],
                # response_model=List[BaseLookupSchema],  # type: ignore
                tags=self.tags,
                # summary='Lookup',
                # dependencies=True,
                # error_responses=[NOT_FOUND],
            )

    def _lookup(self):
        # async def _lookup(db: AsyncSession, find: str = '', **kwargs: Any) -> List[BaseLookupSchema]:
        async def route(
            db: AsyncSession = Depends(self.session),
            find: str = ''
            # db: Session = Depends(self.db_func),
        ) -> List[BaseLookupSchema]:
            return await self.crud._lookup(db, find)


        return route


class BaseFormEndpointCreator(BaseEndpointCreator):

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
        self._deleted_methods.extend([
            'create',
            'read',
            'read_multi',
            'read_paginated',
            'update',
            'delete',
            'db_delete',
        ])

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


        if self.crud and self.crud.form:
            self.add_custom_route(
                path='/',
                endpoint=self._form(),
                methods=['GET'],
                # response_model=List[BaseLookupSchema],  # type: ignore
                tags=self.tags,
                # summary='Lookup',
                # dependencies=True,
                # error_responses=[NOT_FOUND],
            )
            self.add_custom_route(
                path='/{id:int}',
                endpoint=self._form_edit(),
                methods=['GET'],
                # response_model=Any,  # type: ignore
                tags=self.tags,
                # summary='Form edit',
                # dependencies=True,
                # error_responses=[NOT_FOUND],
            )

        if self.crud and self.crud.lista:
            self.add_custom_route(
                path='/lista',
                endpoint=self._form_lista(),
                methods=['GET'],
                # response_model=Any,  # type: ignore
                tags=self.tags,
                # summary='Form lista',
                # dependencies=True,
                # error_responses=[NOT_FOUND],
            )


    def _form(self):
        async def route(
            request: Request, 
            ajax: bool = False,
            default: dict = Depends(utils.parse_list)
        ):
            _schema = _j.generate_json_schema(self.crud.form['schema'])
            _schema = utils.preencher_schema_model(None, _schema, self.crud.get_schema_value, self.crud.get_schema_data_list, self.crud.get_schema_component)
            _schema = utils.preencher_schema_default(default, _schema)
            
            context = {'request': request, 'schema': _schema, 'is_ajax': ajax}
            context.update(request.state.custom_context)

            return templates.TemplateResponse(self.crud.form['template'], context)
        
        return route
    
    def _form_edit(self):
        async def route(
            request: Request,
            # id: self._pk_type,  # type: ignore
            id: int,
            db: AsyncSession = Depends(self.session),
            ajax: bool = False,
            default: dict = Depends(utils.parse_list)
        ):
            # model: Model = db.query(self.db_model).get(item_id)
            model = await self.crud.get(db, id=id)

            if model:
                _schema = self.crud.form['schema']
                _schema = _j.generate_json_schema(_schema)
                _schema = utils.preencher_schema_model(model, _schema, self.crud.get_schema_value, self.crud.get_schema_data_list, self.crud.get_schema_component)
                _schema = utils.set_form_action_id(_schema, id, 'PATCH')
                _schema = utils.preencher_schema_default(default, _schema)

                context = {'request': request, 'schema': _schema, 'is_ajax': ajax}
                context.update(request.state.custom_context)

                return templates.TemplateResponse(self.crud.form['template'], context)
            # else:
                # raise NOT_FOUND from None
            
        return route
    
    def _form_lista(self):
        async def route(
            request: Request, 
            ajax: bool = False,
            default: dict = Depends(utils.parse_list)
        ):
            _schema = _j.generate_json_schema(self.crud.lista['schema'])
            _schema = utils.preencher_schema_model(None, _schema, self.crud.get_schema_value, self.crud.get_schema_data_list, self.crud.get_schema_component)
            _schema = utils.preencher_schema_default(default, _schema)
            
            context = {'request': request, 'schema': _schema, 'is_ajax': ajax}
            context.update(request.state.custom_context)

            return templates.TemplateResponse(self.crud.lista['template'], context)
        
        return route
    
