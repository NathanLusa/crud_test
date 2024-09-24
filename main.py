from typing import AsyncGenerator, List, Any

from fastapi import FastAPI
from fastcrud import crud_router, EndpointCreator, FastCRUD

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from crud_test.item.model import Base, Item
from crud_test.item.schemas import ItemSchema

from core import api_router, CoreCRUD, ApiCRUD, FormCRUD
from core.schemas import BaseLookupSchema


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


def lookup_solver(db_models: List[Item]) -> List[BaseLookupSchema]:
    return [BaseLookupSchema(value=x['id'], desc=x['name']) for x in db_models['data']]

def lookup_filter(find):
    return {'name__ilike':f'%{find}%'}


# CRUD operations setup
item_crud = ApiCRUD(
    Item,
    lookup_filter=lookup_filter,
    lookup_solver=lookup_solver,
)

# CRUD router setup
# item_router = crud_router(
item_router = api_router(
    session=get_session,
    model=Item,
    create_schema=ItemSchema,
    update_schema=ItemSchema,
    crud=item_crud,
    path="/conta",
    tags=["Conta"],
)


item_form_crud = FormCRUD(
    Item,
    lookup_filter=lookup_filter,
    lookup_solver=lookup_solver,
)

item_form_router = api_router(
    session=get_session,
    model=Item,
    create_schema=ItemSchema,
    update_schema=ItemSchema,
    crud=item_form_crud,
    path="/conta",
    tags=["Conta"],
)


app.include_router(item_router, prefix='/api')
app.include_router(item_form_router, prefix='/form')