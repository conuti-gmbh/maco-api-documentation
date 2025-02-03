#!/usr/bin/env python3
import os
import shutil
import yaml

def copy_yaml_files(source_dir: str, target_dir: str):
    """Copy YAML files from source to target directory with PI_ prefix."""
    # Remove existing .yml files in target directory
    for file in os.listdir(target_dir):
        if file.endswith('.yml'):
            os.remove(os.path.join(target_dir, file))
    
    # Copy new files with PI_ prefix
    for file in os.listdir(source_dir):
        if file.endswith('.yaml'):
            source_path = os.path.join(source_dir, file)
            # Change extension to .yml and add PI_ prefix
            new_filename = f"PI_{file[:-5]}.yml"  # Remove .yaml and add .yml
            target_path = os.path.join(target_dir, new_filename)
            
            # Copy and convert the file
            with open(source_path, 'r', encoding='utf-8') as source:
                content = yaml.safe_load(source)
                
            with open(target_path, 'w', encoding='utf-8') as target:
                yaml.dump(content, target, allow_unicode=True, sort_keys=False)
            
            print(f"Copied and converted {file} to {new_filename}")

def update_schema_references(schema_file: str, pis_dir: str):
    """Update the schema file with references to all PI yaml files."""
    # Get list of all PI files
    pi_files = [f for f in os.listdir(pis_dir) if f.endswith('.yml')]
    pi_files.sort()  # Sort to maintain consistent order
    
    # Create new schema content
    schema_content = {
        'oneOf': [
            {'$ref': f'../../components/requestBodies/PIs/{pi_file}'}
            for pi_file in pi_files
        ]
    }
    
    # Write updated schema
    with open(schema_file, 'w', encoding='utf-8') as f:
        yaml.dump(schema_content, f, allow_unicode=True, sort_keys=False)
    
    print(f"Updated schema references in {schema_file}")

def main():
    base_dir = r"d:\DocWorkspace\maco-api-documentation"
    source_dir = os.path.join(base_dir, "pythons", "createPiFromTemplater", "templater", "yaml_output")
    target_dir = os.path.join(base_dir, "macoapp-schreiben", "components", "requestBodies", "PIs")
    schema_file = os.path.join(base_dir, "macoapp-schreiben", "commands", "PROZESSDATEN", "SCHEMAS_REQUESTBODY_PROZESSDATEN.yaml")
    
    # Copy YAML files
    copy_yaml_files(source_dir, target_dir)
    
    # Update schema references
    update_schema_references(schema_file, target_dir)

if __name__ == "__main__":
    main()
