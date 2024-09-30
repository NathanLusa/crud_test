from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, registry, mapped_column


# class Base(DeclarativeBase):
#     pass

table_registry = registry()

@table_registry.mapped_as_dataclass
class Item():
    __tablename__ = "items"
    
    id: Mapped[int]  = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    category: Mapped[str]
    price: Mapped[float]
    last_sold: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())