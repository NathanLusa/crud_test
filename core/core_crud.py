from typing import Optional, Callable, Any, List

from fastcrud import FastCRUD
from fastcrud.types import ModelType
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import BaseLookupSchema

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


    async def _lookup(self, db: AsyncSession, find: str = '', **kwargs: Any) -> Any: #List[BaseLookupSchema]:
        # query = db.query(self.db_model)
        # stmt = await self.select(
        #     schema_to_select=self.model,
        #     # sort_columns=sort_columns,
        #     # sort_orders=sort_orders,
        #     **kwargs,
        # )
        query = await self.get_multi(db)

        # if self.lookup_filter: 
        #     query = self.lookup_filter(query, find)

        # query.order_by(getattr(self.db_model, self._pk))
        # query.limit(limit)
        # query.offset(skip)

        # query = self.lookup_solver(query.all())
        # query = await db.execute(stmt)
        return query
    