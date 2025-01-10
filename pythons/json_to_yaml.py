import json
import yaml
import os

# This script converts a JSON file to a YAML file, starting from the 'data' key.
# To run this script, use the command: python json_to_yaml.py

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def convert_json_to_yaml(input_file, output_file):
    # Load the JSON data from the file
    json_data = load_json(input_file)
    
    yaml_data = {}
    # Extract the 'data' key
    yaml_data['value'] = json_data['data']
    
    # Write the YAML data to the specified file
    write_yaml(yaml_data, output_file)

# Define file paths
input_file = '../pythons/yaml2json/55001_eingehend_Testfall1.json'
output_file = '../pythons/yaml2json/55001_eingehend_Testfall1.yaml'

# Convert the JSON file to a YAML file
convert_json_to_yaml(input_file, output_file)
