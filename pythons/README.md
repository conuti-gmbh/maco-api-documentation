# Python Scripts Documentation

This directory contains various Python scripts used for managing and generating MACO API documentation. Below is a detailed description of each script and its purpose.

## Schema Generation and Management Scripts

### createPiFromTemplater Directory

This directory contains scripts for generating and managing PI (Prüfidentifikator) schemas:

#### `generate_schema.py`
Core script for generating YAML schemas from CSV/TXT files. It:
- Loads paths and EDIFACT mappings from CSV files
- Loads base schema from GitHub
- Creates schema structures with proper types and properties
- Adds process descriptions from processinfo.json
- Handles array types and nested properties
- Resolves schema references

#### `process_all_files.py`
Batch processing script that:
- Processes all .txt files in the templater directory
- Uses generate_schema.py logic for each file
- Creates corresponding YAML schema files in yaml_output directory
- Maintains the mapping between paths and their EDIFACT codes

#### `convert_to_yaml.py`
Simple conversion utility that:
- Reads .txt files containing path and EDIFACT mappings
- Converts them to YAML format
- Preserves the mapping between paths and their EDIFACT codes

#### `update_schemas.py`
Script for updating the production schema files:
- Copies generated YAML files to macoapp-schreiben/components/requestBodies/PIs
- Adds PI_ prefix to filenames
- Updates SCHEMAS_REQUESTBODY_PROZESSDATEN.yaml with new references
- Manages file organization and schema references

## Other Utility Scripts

### `generate_examples_for_processDaten.py`
Script for generating example data for process data:
- Creates example data structures based on schema definitions
- Used for documentation and testing purposes

### `generate_pi_yaml.py`
Utility for PI YAML file generation:
- Creates or updates PI-specific YAML files
- Handles schema structure and validation

### `json_to_yaml.py`
Conversion utility that:
- Converts JSON files to YAML format
- Maintains data structure and formatting

### `sort_yaml.py`
YAML file organization script that:
- Sorts YAML file contents
- Maintains consistent ordering of elements
- Improves readability and maintainability

### `update_processinfo.py`
Script for managing process information:
- Updates processinfo.json with new process data
- Maintains process descriptions and metadata

## Usage

Most scripts can be run directly from the command line. For example:

```bash
# Generate schemas from template files
python createPiFromTemplater/process_all_files.py

# Update production schemas
python createPiFromTemplater/update_schemas.py

# Sort YAML files
python sort_yaml.py
```

## Dependencies

These scripts require the following Python packages:
- pyyaml: For YAML file handling
- requests: For making HTTP requests
- typing: For type hints and annotations

## Note

Always run these scripts from the root directory of the documentation project to ensure proper path resolution.
