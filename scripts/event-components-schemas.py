import yaml
import os

def create_schema_files(openapi_file):
    with open(openapi_file, 'r') as f:
        openapi_data = yaml.safe_load(f)

    schemas_dir = 'schemas'
    if not os.path.exists(schemas_dir):
        os.makedirs(schemas_dir)

    index_data = {}
    for schema_name, schema_data in openapi_data['components']['schemas'].items():
        # Create a file for the schema
        with open(os.path.join(schemas_dir, f'{schema_name}.yml'), 'w') as f:
            yaml.dump({schema_name: schema_data}, f, default_flow_style=False)

        # Add the file to the index
        index_data[schema_name] = {'$ref': f'{schema_name}.yml'}

    # Create the _index.yml file
    with open(os.path.join(schemas_dir, '_index.yml'), 'w') as f:
        yaml.dump(index_data, f, default_flow_style=False)

if __name__ == '__main__':
    create_schema_files('events-openapi.yaml')
