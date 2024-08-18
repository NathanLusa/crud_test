from typing import AsyncGenerator

from fastapi import FastAPI
from fastcrud import crud_router

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from crud_test.item.model import Base, Item
from crud_test.item.schemas import CreateItemSchema, UpdateItemSchema

from core import core_router, CoreCRUD

# Database setup (Async SQLAlchemy)
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Database session dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Create tables before the app start
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# FastAPI app
app = FastAPI(lifespan=lifespan)

# CRUD operations setup
item_crud = CoreCRUD(Item)

# CRUD router setup
# item_router = crud_router(
item_router = core_router(
    session=get_session,
    model=Item,
    create_schema=CreateItemSchema,
    update_schema=UpdateItemSchema,
    crud=item_crud,
    path="/item",
    tags=["Items"],
)

app.include_router(item_router, prefix='/api')