from typing import AsyncGenerator, List, Any

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from fastcrud import crud_router, EndpointCreator, FastCRUD

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from crud_test.item.model import Base, Item
from crud_test.item.schemas import ItemSchema

from core import api_router, form_router, ApiCRUD, FormCRUD
from core import components as c
from core.schemas import BaseLookupSchema
from core.templates import templates, MenuItem
from core.types import BaseUI, TemplateSchemaDict

from app.enums import ContaStatusEnum, ContaTipoEnum


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
app.mount('/static', StaticFiles(directory='core/static'), name='static')

menus = [
    MenuItem(name='Home', description='Home', base_endpoint='/', endpoint='/'),
    MenuItem(name='Conta', description='Conta', base_endpoint='/form/conta', endpoint='/form/conta/lista'),
    MenuItem(name='Imovel', description='Imovel', base_endpoint='/form/imovel', endpoint='/form/imovel/lista'),
    MenuItem(name='Usuario', description='Usuario', base_endpoint='/form/usuario', endpoint='/form/usuario/lista'),
]

@app.middleware("http")
async def add_menu_context_form(request: Request, call_next):
    _menus = None
    if (request.url.path == '/') or (request.url.path.split('/')[1] == 'form'):
        _menus = menus

        for item in _menus:
            if item.base_endpoint == '/':
                item.active = request.url.path == '/'
            else:
                item.active = item.base_endpoint in request.url.path

    # if request.url.query:
    #     print(type(request.url.query), request.url.query)
    request.state.custom_context = {'menu': _menus}

    response = await call_next(request)
    return response




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






class ContaListaSchema(BaseUI):
    title: str = 'Contas'
    div: c.Div = c.Div(
        components=[
            c.Table(
                title=[
                    c.Link(href='/form/conta', components=[c.Text(text='Novo')], class_name='btn btn-primary btn-sm'),
                ],
                data_list=[
                    c.DataAttr(name='api-url', value='/api/conta'),
                    c.DataAttr(name='form-url', value='/form/conta'),
                    c.DataAttr(name='table-url', value='/api/conta'),
                ],
                form_url='/contas',
                columns=[
                    c.TableColumn(name='#', data_list=[c.DataAttr(name='field', value='id')]),
                    c.TableColumn(name='Nome', data_list=[c.DataAttr(name='field', value='name')]),
                    c.TableColumn(name='Tipo', data_list=[c.DataAttr(name='field', value='type')]),
                    c.TableColumn(name='Usuário', data_list=[c.DataAttr(name='field', value='usuario'), c.DataAttr(name='lookup-url', value='/api/usuario/')]),
                    c.TableColumn(name='Status', data_list=[c.DataAttr(name='field', value='status')]),
                    c.TableColumn(
                        name='Actions', 
                        data_list=[c.DataAttr(name='field', value='actions')],
                        action_list=['edit', 'delete'],
                    ),
                ]
            ),       
        ]
    )


class ContaFormSchema(BaseUI):
    title: str = 'Conta'
    form: c.Form = c.Form(
        title = 'Conta',
        action='/api/conta',
        method='POST',
        post_type='JSON',
        components=[
            c.Input(title='Name', html_type='text', name='name', value='', placeholder='Nome', required=True),
            c.Select(title='Type', name='type', options=[c.SelectOption(label=x, value=x) for x in ContaTipoEnum], required=True),
            c.Select(title='Status', name='status', options=[c.SelectOption(label=x, value=x) for x in ContaStatusEnum], required=True),
            c.Lookup(title='Usuário', name='usuario', required=False, data_list=[c.DataAttr(name='lookup-url', value='/api/usuario/lookup/')]),

            c.Button(name='submit', label='Gravar', html_type='submit'),
            c.Link(href='/', class_name='btn btn-secondary btn-sm', components=[c.Text(text='Fechar')]),
        ]
    )


def get_schema_data_list(name, default: List[c.DataAttr], id):
    if name == 'imagens':
        default.append(
            c.DataAttr(
                name='images', 
                value=';'.join([
                    'https://mdn.github.io/learning-area/html/multimedia-and-embedding/tasks/images/larch.jpg',
                    'https://mdn.github.io/learning-area/html/multimedia-and-embedding/tasks/images/larch.jpg',
                ])
            )
        )

    return default


item_form_crud = FormCRUD(
    Item,
    form=TemplateSchemaDict(template='form.html', schema=ContaFormSchema),
    lista=TemplateSchemaDict(template='form.html', schema=ContaListaSchema),
    get_schema_data_list=get_schema_data_list,
)

item_form_router = form_router(
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