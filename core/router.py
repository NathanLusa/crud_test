
from typing import Type, Optional, Union, Sequence, Callable
from enum import Enum

from fastapi import APIRouter
from fastcrud import crud_router, FilterConfig
from fastcrud.types import (
    CreateSchemaType,
    DeleteSchemaType,
    ModelType,
    UpdateSchemaType,
)

from core import CoreCRUD, APIEndpointCreator, FormEndpointCreator


def api_router(
    session: Callable,
    model: ModelType,
    create_schema: Type[CreateSchemaType],
    update_schema: Type[UpdateSchemaType],
    crud: Optional[CoreCRUD] = None,
    delete_schema: Optional[Type[DeleteSchemaType]] = None,
    path: str = "",
    tags: Optional[list[Union[str, Enum]]] = None,
    include_in_schema: bool = True,
    create_deps: Sequence[Callable] = [],
    read_deps: Sequence[Callable] = [],
    read_multi_deps: Sequence[Callable] = [],
    read_paginated_deps: Sequence[Callable] = [],
    update_deps: Sequence[Callable] = [],
    delete_deps: Sequence[Callable] = [],
    db_delete_deps: Sequence[Callable] = [],
    included_methods: Optional[list[str]] = None,
    deleted_methods: Optional[list[str]] = None,
    endpoint_creator: Optional[Type[APIEndpointCreator]] = None,
    is_deleted_column: str = "is_deleted",
    deleted_at_column: str = "deleted_at",
    updated_at_column: str = "updated_at",
    endpoint_names: Optional[dict[str, str]] = None,
    filter_config: Optional[Union[FilterConfig, dict]] = None,
) -> APIRouter:
    _endpoint_creator = endpoint_creator or APIEndpointCreator

    return crud_router(
        session=session,
        model=model,
        create_schema=create_schema,
        update_schema=update_schema,
        crud=crud,
        delete_schema=delete_schema,
        path=path,
        tags=tags,
        include_in_schema=include_in_schema,
        create_deps=create_deps,
        read_deps=read_deps,
        read_multi_deps=read_multi_deps,
        read_paginated_deps=read_paginated_deps,
        update_deps=update_deps,
        delete_deps=delete_deps,
        db_delete_deps=db_delete_deps,
        included_methods=included_methods,
        deleted_methods=deleted_methods,
        endpoint_creator=_endpoint_creator,
        is_deleted_column=is_deleted_column,
        deleted_at_column=deleted_at_column,
        updated_at_column=updated_at_column,
        endpoint_names=endpoint_names,
        filter_config=filter_config,
    )

def form_router(
    session: Callable,
    model: ModelType,
    create_schema: Type[CreateSchemaType],
    update_schema: Type[UpdateSchemaType],
    crud: Optional[CoreCRUD] = None,
    delete_schema: Optional[Type[DeleteSchemaType]] = None,
    path: str = "",
    tags: Optional[list[Union[str, Enum]]] = None,
    include_in_schema: bool = True,
    create_deps: Sequence[Callable] = [],
    read_deps: Sequence[Callable] = [],
    read_multi_deps: Sequence[Callable] = [],
    read_paginated_deps: Sequence[Callable] = [],
    update_deps: Sequence[Callable] = [],
    delete_deps: Sequence[Callable] = [],
    db_delete_deps: Sequence[Callable] = [],
    included_methods: Optional[list[str]] = None,
    deleted_methods: Optional[list[str]] = None,
    endpoint_creator: Optional[Type[FormEndpointCreator]] = None,
    is_deleted_column: str = "is_deleted",
    deleted_at_column: str = "deleted_at",
    updated_at_column: str = "updated_at",
    endpoint_names: Optional[dict[str, str]] = None,
    filter_config: Optional[Union[FilterConfig, dict]] = None,
) -> APIRouter:
    _endpoint_creator = endpoint_creator or FormEndpointCreator

    return crud_router(
        session=session,
        model=model,
        create_schema=create_schema,
        update_schema=update_schema,
        crud=crud,
        delete_schema=delete_schema,
        path=path,
        tags=tags,
        include_in_schema=include_in_schema,
        create_deps=create_deps,
        read_deps=read_deps,
        read_multi_deps=read_multi_deps,
        read_paginated_deps=read_paginated_deps,
        update_deps=update_deps,
        delete_deps=delete_deps,
        db_delete_deps=db_delete_deps,
        included_methods=included_methods,
        deleted_methods=deleted_methods,
        endpoint_creator=_endpoint_creator,
        is_deleted_column=is_deleted_column,
        deleted_at_column=deleted_at_column,
        updated_at_column=updated_at_column,
        endpoint_names=endpoint_names,
        filter_config=filter_config,
    )