import yaml
import os

def create_path_files(openapi_file):
    """
    Create separate YAML files for each path in the OpenAPI file.

    Args:
        openapi_file (str): Path to the OpenAPI YAML file.
    """
    with open(openapi_file, 'r', encoding='utf-8') as f:
        openapi_data = yaml.safe_load(f)

    paths_dir = 'processMappingGenerated/paths'
    if not os.path.exists(paths_dir):
        os.makedirs(paths_dir)

    index_data = {}
    for path, path_data in openapi_data['paths'].items():
        # Remove leading '/' and replace '/' with '_' to create a valid filename
        filename = path[1:].replace('/', '_')
        filename = filename.replace('-', '_')  # Replace '-' with '_' to avoid issues

        # Create a directory for the path if it contains '/'
        path_dir = os.path.join(paths_dir, os.path.dirname(path[1:]))
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)

        # Create a file for the path
        with open(os.path.join(paths_dir, path[1:] + '.yml'), 'w', encoding='utf-8') as f:
            yaml.dump({path: path_data}, f, default_flow_style=False, allow_unicode=True)

        # Add the file to the index
        index_data[path] = {'$ref': path[1:] + '.yml'}

    # Create the _index.yml file
    with open(os.path.join(paths_dir, '_index.yml'), 'w', encoding='utf-8') as f:
        yaml.dump(index_data, f, default_flow_style=False, allow_unicode=True)

if __name__ == '__main__':
    create_path_files('processMappingGenerated.yaml')
