from typing import List, Optional

from fastapi import Query
from core.components.attribute import DataAttr

def preencher_schema_model_object(model, schema_json, get_schema_value, get_schema_data_list, get_schema_component):
    def fill_component(component, model):
        if 'name' in component:
            if model and hasattr(model, component['name']):
                component['value'] = str(getattr(model, component['name']))            
                if hasattr(model, f'{component["name"]}_rel'):
                    relation = getattr(model, f'{component["name"]}_rel')
                    component['data_list'].append(DataAttr(name='selected-id', value=str(getattr(model, component['name']))))
                    if hasattr(relation, 'name'):
                        component['value'] += (' - ' + relation.name)

            if get_schema_value and ('value' in component):
                component['value'] = get_schema_value(component['name'], component['value'], model['id'] if model else 0)

            if get_schema_data_list and ('data_list' in component):
                component['data_list'] = get_schema_data_list(component['name'], component['data_list'], model['id'] if model else 0)

        if get_schema_component:
            component = get_schema_component(component, model['id'] if model else 0)

        if 'components' in component:
            for sub_component in component['components']:
                fill_component(sub_component, model)

        if 'title' in component and isinstance(component['title'], list):
            for sub_component in component['title']:
                fill_component(sub_component, model)


    # Procurar pela chave 'components' no schema
    def traverse_and_fill(schema, model):
        if isinstance(schema, dict):
            for key, value in schema.items():
                if key == 'components' and isinstance(value, list):
                    for component in value:
                        fill_component(component, model)
                else:
                    traverse_and_fill(value, model)

            if get_schema_component:
                schema = get_schema_component(schema, model['id'] if model else 0)
        elif isinstance(schema, list):
            for item in schema:
                traverse_and_fill(item, model)

    traverse_and_fill(schema_json, model)

    return schema_json


def preencher_schema_model(model, schema_json, get_schema_value, get_schema_data_list, get_schema_component):
    def fill_component(component, model):
        if 'name' in component:
            if model and component['name'] in model:
                component['value'] = str(model[component['name']])
                if f'{component["name"]}_rel' in model:
                    relation = model[f'{component["name"]}_rel']
                    component['data_list'].append(DataAttr(name='selected-id', value=str(model[component['name']])))
                    if 'name' in relation:
                        component['value'] += (' - ' + relation.name)

            if get_schema_value and ('value' in component):
                component['value'] = get_schema_value(component['name'], component['value'], model['id'] if model else 0)

            if get_schema_data_list and ('data_list' in component):
                component['data_list'] = get_schema_data_list(component['name'], component['data_list'], model['id'] if model else 0)

        if get_schema_component:
            component = get_schema_component(component, model['id'] if model else 0)

        if 'components' in component:
            for sub_component in component['components']:
                fill_component(sub_component, model)

        if 'title' in component and isinstance(component['title'], list):
            for sub_component in component['title']:
                fill_component(sub_component, model)


    # Procurar pela chave 'components' no schema
    def traverse_and_fill(schema, model):
        if isinstance(schema, dict):
            for key, value in schema.items():
                if key == 'components' and isinstance(value, list):
                    for component in value:
                        fill_component(component, model)
                else:
                    traverse_and_fill(value, model)

            if get_schema_component:
                schema = get_schema_component(schema, model['id'] if model else 0)
        elif isinstance(schema, list):
            for item in schema:
                traverse_and_fill(item, model)

    traverse_and_fill(schema_json, model)

    return schema_json


def set_form_action_id(schema_json, id, method):
    # Procurar pela chave 'components' no schema
    def traverse_and_fill(schema):
        if isinstance(schema, dict):
            for key, value in schema.items():
                if key == 'form' and isinstance(value, dict):
                    for component in value:
                        if 'default' in component:
                            traverse_and_fill(value['default'])
                        elif 'action' in component:
                            value['action'] += f'/{id}'
                        elif 'method' in component:
                            value['method'] = method
                elif key == 'action':
                    schema['action'] += f'/{id}'
                elif key == 'method':
                    schema['method'] = method
                else:
                    traverse_and_fill(value)
        elif isinstance(schema, list):
            for item in schema:
                traverse_and_fill(item)

    traverse_and_fill(schema_json)
    # print('FORM 1: ', schema_json)
    return schema_json


def preencher_schema_default(default, schema_json):
    def fill_component(component, default):
        if 'name' in component:
            if default and component['name'] in default:
                component['value'] = default[component['name']]
                # if hasattr(model, f'{component["name"]}_rel'):
                #     relation = getattr(model, f'{component["name"]}_rel')
                #     component['data_list'].append(DataAttr(name='selected-id', value=str(getattr(model, component['name']))))
                #     if hasattr(relation, 'name'):
                #         component['value'] += (' - ' + relation.name)

        if 'components' in component:
            for sub_component in component['components']:
                fill_component(sub_component, default)

        if 'title' in component and isinstance(component['title'], list):
            for sub_component in component['title']:
                fill_component(sub_component, default)

    # Procurar pela chave 'components' no schema
    def traverse_and_fill(schema, default):
        if isinstance(schema, dict):
            for key, value in schema.items():
                if key == 'components' and isinstance(value, list):
                    for component in value:
                        fill_component(component, default)
                else:
                    traverse_and_fill(value, default)
        elif isinstance(schema, list):
            for item in schema:
                traverse_and_fill(item, default)

    traverse_and_fill(schema_json, default)

    return schema_json



def parse_list(default: List[str] = Query(None)) -> Optional[List]:

    def remove_prefix(text: str, prefix: str):
        return text[text.startswith(prefix) and len(prefix):]

    def remove_postfix(text: str, postfix: str):
        if text.endswith(postfix):
            text = text[:-len(postfix)]
        return text
    
    if default is None:
        return

    # we already have a list, we can return
    if len(default) > 1:
        return default

    # if we don't start with a "[" and end with "]" it's just a normal entry
    flat_names = default[0]
    if not flat_names.startswith("[") and not flat_names.endswith("]"):
        return default

    flat_names = remove_prefix(flat_names, "[")
    flat_names = remove_postfix(flat_names, "]")

    _list = flat_names.split(",")
    _list = [remove_prefix(n.strip(), "\"") for n in _list]
    _list = [remove_postfix(n.strip(), "\"") for n in _list]

    result = {}
    for item in _list:
        item = item.split(':')
        result.update({item[0]: item[1]})

    return result