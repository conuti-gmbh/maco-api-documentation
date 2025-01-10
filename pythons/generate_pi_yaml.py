import yaml
import os

# This script reads specified items from '55001_eingehend_Testfall1.yaml' and writes them to a new file in the format specified in 'PI_55001.yml'.
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

    # Extract the required items from the input file
    required_items = ['BILANZIERUNG', 'ENERGIELIEFERVERTRAG', 'MARKTLOKATION', 'MESSLOKATION', 'NETZNUTZUNGSVERTRAG']
    extracted_data = {item: input_data['value']['stammdaten'][item] for item in required_items if item in input_data['value']['stammdaten']}

    # Prepare the output data in the required format
    output_data = {
        'type': 'object',
        'properties': {
            'stammdaten': {
                'type': 'object',
                'properties': {item: stammdaten_data['properties']['stammdaten']['properties'][item] for item in extracted_data}
            },
            'transaktionsdaten': input_data['value']['transaktionsdaten']
        }
    }

    # Write the output data to the specified file
    write_yaml(output_data, output_file)

# Define file paths
input_file = '../macoapp-schreiben/components/examples/Strom/55001_eingehend_Testfall1.yaml'
stammdaten_file = '../bo4e/components/requestBodies/stammdaten.yml'
output_file = '../macoapp-schreiben/components/requestBodies/PIs/PI_55001.yml'

# Generate the PI YAML file
generate_pi_yaml(input_file, stammdaten_file, output_file)
