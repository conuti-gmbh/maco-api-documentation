#!/usr/bin/env python3
import os
from generate_schema import (
    load_csv_paths,
    load_base_schema,
    load_process_info,
    create_schema_structure,
    add_process_descriptions
)
import yaml

def process_file(input_file: str, output_dir: str, process_info_file: str):
    """Process a single input file and generate the corresponding schema."""
    # Extract the five-digit number (pruefidentifikator)
    base_name = os.path.basename(input_file)
    pruefidentifikator = base_name.split('.')[0]
    
    output_file = os.path.join(output_dir, f"{pruefidentifikator}.yaml")
    
    # Load required paths and EDIFACT mappings from the input file
    required_paths, edifact_mappings = load_csv_paths(input_file)
    
    # Load the base schema
    base_schema = load_base_schema()
    
    # Load process info
    process_map = load_process_info(process_info_file)
    
    # Create schema structure
    schema = create_schema_structure(base_schema, required_paths, edifact_mappings)
    
    # Add process descriptions
    add_process_descriptions(schema, process_map, pruefidentifikator)
    
    # Write the final schema to file
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(schema, f, allow_unicode=True, sort_keys=False)
    
    print(f"Generated schema saved to {output_file}")

def main():
    """Process all txt files in the templater directory."""
    base_dir = r"d:\DocWorkspace\maco-api-documentation"
    templater_dir = os.path.join(base_dir, "pythons", "createPiFromTemplater", "templater")
    output_dir = os.path.join(templater_dir, "yaml_output")
    process_info_file = os.path.join(base_dir, "pythons", "processinfo.json")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all txt files
    for filename in os.listdir(templater_dir):
        if filename.endswith('.txt'):
            input_file = os.path.join(templater_dir, filename)
            process_file(input_file, output_dir, process_info_file)

if __name__ == "__main__":
    main()
