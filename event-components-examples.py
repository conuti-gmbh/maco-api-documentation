import yaml
import os

def create_example_files(openapi_file):
    with open(openapi_file, 'r') as f:
        openapi_data = yaml.safe_load(f)

    examples_dir = 'events/components/examples'
    if not os.path.exists(examples_dir):
        os.makedirs(examples_dir)

    index_data = {}
    for example_name, example_data in openapi_data['components']['examples'].items():
        # Create a file for the example
        with open(os.path.join(examples_dir, f'{example_name}.yml'), 'w') as f:
            yaml.dump({example_name: example_data}, f, default_flow_style=False)

        # Add the file to the index
        index_data[example_name] = {'$ref': f'{example_name}.yml'}

    # Create the _index.yml file
    with open(os.path.join(examples_dir, '_index.yml'), 'w') as f:
        yaml.dump(index_data, f, default_flow_style=False)

if __name__ == '__main__':
    create_example_files('events-openapi.yaml')
