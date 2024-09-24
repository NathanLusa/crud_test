from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

from core.context_processors import processors


class MenuItem(BaseModel):
    name: str
    description: str
    base_endpoint: str
    endpoint: str
    active: bool = False
    class_name: str = ''

templates = Jinja2Templates(directory='core/templates')
for x in processors:
    templates.env.globals[x.__name__] = x
