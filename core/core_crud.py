from fastcrud import FastCRUD
from fastcrud.types import ModelType


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