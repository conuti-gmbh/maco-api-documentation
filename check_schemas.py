import yaml
import os

def check_schemas(openapi_file, schemas_folder):
    with open(openapi_file, 'r') as f:
        openapi = yaml.safe_load(f)

    schemas = openapi.get('components', {}).get('schemas', {})

    missing_schemas = []

    for schema_name, schema in schemas.items():
        schema_file = os.path.join(schemas_folder, f'{schema_name}.yml')
        if not os.path.exists(schema_file):
            missing_schemas.append(schema_name)

    if missing_schemas:
        print(f'The following schemas are missing in the {schemas_folder} folder:')
        for schema_name in missing_schemas:
            print(schema_name)
    else:
        print('All schemas exist in the schemas folder.')

if __name__ == '__main__':
    openapi_file = '_openapi.yaml'
    schemas_folder = 'schemas/'
    check_schemas(openapi_file, schemas_folder)
