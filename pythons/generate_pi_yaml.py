import yaml
import os
import re

# This script reads specified items from all YAML files in the specified folder and writes them to new files in the required format.
# To run this script, use the command: python generate_pi_yaml.py

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def write_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def generate_pi_yaml(input_file, stammdaten_file, output_file):
    # Load the input YAML files
    input_data = load_yaml(input_file)
    stammdaten_data = load_yaml(stammdaten_file)

    # Dynamically determine the required items from the input file
    required_items = input_data['value']['stammdaten'].keys()
    extracted_data = {item: input_data['value']['stammdaten'][item] for item in required_items if item in input_data['value']['stammdaten']}

    # Prepare the output data in the required format
    output_data = {
        'type': 'object',
        'properties': {
            'stammdaten': {
                'type': 'object',
                'properties': {item: stammdaten_data['properties']['stammdaten']['properties'][item] for item in extracted_data}
            },
            'transaktionsdaten': stammdaten_data['properties']['transaktionsdaten']
        }
    }

    # Write the output data to the specified file
    write_yaml(output_data, output_file)

def process_all_files(input_folder, stammdaten_file, output_folder):
    # Get all YAML files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith("_eingehend_Testfall1.yaml"):
            # Extract the PI number from the filename
            pi = re.search(r'(\d+)_eingehend_Testfall1.yaml', filename).group(1)
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, f"PI_{pi}.yml")
            generate_pi_yaml(input_file, stammdaten_file, output_file)

# Define file paths
input_folder = "../macoapp-schreiben/components/examples/Strom/"
stammdaten_file = "../macoapp-schreiben/components/requestBodies/stammdaten.yml"
output_folder = "../macoapp-schreiben/components/requestBodies/PIs/"

# Process all files in the input folder
process_all_files(input_folder, stammdaten_file, output_folder)
