#!/usr/bin/env python3
import os
import yaml

def convert_to_yaml(input_file):
    yaml_data = {}
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                # Split the line into path and mapping
                parts = line.split(';')
                if len(parts) >= 2:
                    path = parts[0].strip()
                    mapping = parts[1].strip()
                    yaml_data[path] = mapping

    return yaml_data

def process_directory(directory):
    # Create yaml_output subdirectory if it doesn't exist
    output_dir = os.path.join(directory, 'yaml_output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all .txt files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            # Extract the five-digit number from the filename
            number = filename[:5]
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(output_dir, f"{number}.yaml")
            
            # Convert and save
            yaml_data = convert_to_yaml(input_path)
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    directory = r"d:\DocWorkspace\maco-api-documentation\pythons\createPiFromTemplater\templater"
    process_directory(directory)
