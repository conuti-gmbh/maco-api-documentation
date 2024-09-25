import yaml
import os

def create_schema(schema_name, schema):
    schema_file = os.path.join('schemas/', f'{schema_name}.yml')
    with open(schema_file, 'w') as f:
        yaml.dump(schema, f, default_flow_style=False)

def check_schemas(openapi_file, schemas_folder):
    with open(openapi_file, 'r') as f:
        openapi = yaml.safe_load(f)

    schemas = openapi.get('components', {}).get('schemas', {})

    missing_schemas = []

    for schema_name, schema in schemas.items():
        schema_file = os.path.join(schemas_folder, f'{schema_name}.yml')
        if not os.path.exists(schema_file):
            missing_schemas.append((schema_name, schema))

    if missing_schemas:
        print(f'The following schemas are missing in the {schemas_folder} folder:')
        for schema_name, schema in missing_schemas:
            print(schema_name)
            create_schema(schema_name, schema)
            print(f'Schema {schema_name} created.')
    else:
        print('All schemas exist in the schemas folder.')

if __name__ == '__main__':
    openapi_file = '_openapi.yaml'
    schemas_folder = 'schemas/'
    if not os.path.exists(schemas_folder):
        os.makedirs(schemas_folder)
    check_schemas(openapi_file, schemas_folder)
