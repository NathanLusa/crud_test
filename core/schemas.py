from pydantic import BaseModel
from typing import Optional, List


class BaseSchema(BaseModel):
    id: int

    class Config:
        orm_mode = True


class BaseStatusSchema(BaseSchema):
    status: int


class BaseLookupSchema(BaseModel):
    value: str | int
    desc: str
    attrs: Optional[dict[str, str]] = {}
