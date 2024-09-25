import yaml
import os

def write_schemas(openapi_file, output_dir):
    """
    Reads an OpenAPI YAML file and writes each schema to a separate file.

    Args:
        openapi_file (str): Path to the OpenAPI YAML file.
        output_dir (str): Directory where schema files will be written.
    """
    with open(openapi_file, 'r') as f:
        openapi = yaml.safe_load(f)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get the schemas from the OpenAPI definition
    schemas = openapi.get('components', {}).get('schemas', {})

    for schema_name, schema in schemas.items():
        # Create a file for each schema
        filename = f"{schema_name}.yml"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w') as f:
            # Write the schema to the file
            yaml.dump(schema, f, default_flow_style=False)

        print(f"Schema '{schema_name}' written to '{filename}'")

if __name__ == "__main__":
    openapi_file = "_openapi.yml"
    output_dir = "schemas"
    write_schemas(openapi_file, output_dir)
