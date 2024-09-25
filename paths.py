import yaml
import os

def write_paths(openapi_file, output_dir):
    """
    Reads an OpenAPI YAML file and writes each path to a separate file.

    Args:
        openapi_file (str): Path to the OpenAPI YAML file.
        output_dir (str): Directory where path files will be written.
    """
    with open(openapi_file, 'r') as f:
        openapi = yaml.safe_load(f)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get the paths from the OpenAPI definition
    paths = openapi.get('paths', {})

    for path, methods in paths.items():
        # Create a file for each path
        filename = f"{path.replace('/', '').replace('{', '').replace('}', '')}.yml"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w') as f:
            # Write the path to the file
            yaml.dump(methods, f, default_flow_style=False)

        print(f"Path '{path}' written to '{filename}'")

if __name__ == "__main__":
    openapi_file = "_openapi.yml"
    output_dir = "paths"
    write_paths(openapi_file, output_dir)
