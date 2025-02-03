#!/usr/bin/env python3
import requests
import yaml
from typing import Dict, Any, List, Set, Tuple, Optional
import copy
import csv
import json

def load_csv_paths(csv_file: str) -> Tuple[Set[str], Dict[str, str]]:
    """Load JSON paths and their EDIFACT mappings from CSV file."""
    paths = set()
    edifact_mappings = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if row and row[0].strip():  # Skip empty lines
                path = row[0].strip()
                edifact = row[1].strip() if len(row) > 1 else ''
                paths.add(path)
                edifact_mappings[path] = edifact
    return paths, edifact_mappings

def load_base_schema() -> Dict[str, Any]:
    """Load the complete schema from GitHub."""
    url = "https://raw.githubusercontent.com/conuti-gmbh/bo4e-schema/master/docs/openapi.yaml"
    response = requests.get(url)
    yaml_content = yaml.safe_load(response.text)
    
    # Get the components/schemas section which contains all our definitions
    schemas = yaml_content.get('components', {}).get('schemas', {})
    
    # Get paths to find message schemas
    paths = yaml_content.get('paths', {})
    for path_item in paths.values():
        for operation in path_item.values():
            if 'requestBody' in operation:
                content = operation['requestBody'].get('content', {})
                for media_content in content.values():
                    if 'schema' in media_content:
                        schema = media_content['schema']
                        if 'properties' in schema:
                            schemas.update(schema['properties'])
            if 'responses' in operation:
                for response in operation['responses'].values():
                    if 'content' in response:
                        for media_content in response['content'].values():
                            if 'schema' in media_content:
                                schema = media_content['schema']
                                if 'properties' in schema:
                                    schemas.update(schema['properties'])
    
    print(f"Loaded {len(schemas)} schema definitions")
    return schemas

def extract_components_from_paths(paths: Set[str]) -> Dict[str, Set[str]]:
    """Extract top-level components from CSV paths."""
    components = {}
    for path in paths:
        parts = path.split('.')
        if len(parts) >= 2:  # Must have at least top-level and component
            top_level = parts[0]
            component = parts[1].split('[')[0]  # Remove array notation
            if top_level not in components:
                components[top_level] = set()
            components[top_level].add(component)
    return components

def find_schema_definition(name: str, base_schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Find a schema definition by name, trying different variations."""
    # Try exact match
    if name in base_schema:
        return base_schema[name]
    
    # Try case-insensitive match
    name_lower = name.lower()
    for key, schema in base_schema.items():
        if key.lower() == name_lower:
            return schema
        # Check if the key ends with our name (e.g. "BOMarktlokation" for "MARKTLOKATION")
        if key.lower().endswith(name_lower):
            return schema
    
    return None

def get_schema_component(name: str, base_schema: Dict[str, Any], required_paths: Set[str], edifact_mappings: Dict[str, str], current_path: str = '') -> Dict[str, Any]:
    """Get a schema component by resolving all its references."""
    # Try to find existing schema definition
    existing_schema = find_schema_definition(name, base_schema)
    
    # For business objects, create or enhance the BO schema
    if name.isupper():
        bo_schema = {
            'type': 'object',
            'title': name.capitalize()
        }
        
        # If we found an existing schema, copy its properties and merge with our base BO properties
        if existing_schema:
            bo_schema.update(existing_schema)
            if 'properties' in existing_schema:
                bo_schema['properties'] = existing_schema['properties'].copy()
        
        # Ensure we have the basic BO properties
        if 'properties' not in bo_schema:
            bo_schema['properties'] = {}
        
        # Special handling for contract types
        if name in ['ENERGIELIEFERVERTRAG', 'NETZNUTZUNGSVERTRAG', 'MESSSTELLEBETREIBSVERTRAG']:
            bo_schema['properties']['boTyp'] = {
                'type': 'string',
                'title': 'BOTyp',
                'description': 'Typ des BO',
                'enum': ['VERTRAG']
            }
            
            # Add vertragsnummer field for contracts
            bo_schema['properties']['vertragsnummer'] = {
                'type': 'string',
                'description': 'Vertragsnummer'
            }
            
            # Add specific contract fields
            if name == 'ENERGIELIEFERVERTRAG':
                bo_schema['properties']['vertragsart'] = {
                    'type': 'string',
                    'description': 'Art des Vertrags',
                    'enum': ['ENERGIELIEFERVERTRAG']
                }
            elif name == 'NETZNUTZUNGSVERTRAG':
                bo_schema['properties']['vertragsart'] = {
                    'type': 'string',
                    'description': 'Art des Vertrags',
                    'enum': ['NETZNUTZUNGSVERTRAG']
                }
            elif name == 'MESSSTELLEBETREIBSVERTRAG':
                bo_schema['properties']['vertragsart'] = {
                    'type': 'string',
                    'description': 'Art des Vertrags',
                    'enum': ['MESSSTELLEBETREIBSVERTRAG']
                }
        else:
            bo_schema['properties']['boTyp'] = {
                'type': 'string',
                'title': 'BOTyp',
                'description': 'Typ des BO',
                'enum': [name]
            }
        
        bo_schema['properties']['versionStruktur'] = {
            'type': 'string',
            'description': 'versionStruktur',
            'default': '1'
        }
        
        if 'required' not in bo_schema:
            bo_schema['required'] = []
        if 'boTyp' not in bo_schema['required']:
            bo_schema['required'].append('boTyp')
        if 'versionStruktur' not in bo_schema['required']:
            bo_schema['required'].append('versionStruktur')
        
        # For contracts, add vertragsart to required fields
        if name in ['ENERGIELIEFERVERTRAG', 'NETZNUTZUNGSVERTRAG', 'MESSSTELLEBETREIBSVERTRAG']:
            if 'vertragsart' not in bo_schema['required']:
                bo_schema['required'].append('vertragsart')
        
        return bo_schema
    
    # For non-BO components, use existing schema or create basic one
    if existing_schema:
        component = existing_schema.copy()
    else:
        # Try to find schema in properties of other schemas
        for schema in base_schema.values():
            if isinstance(schema, dict) and 'properties' in schema:
                props = schema['properties']
                if name in props:
                    component = props[name].copy()
                    break
                # Try case-insensitive match
                name_lower = name.lower()
                for key, prop in props.items():
                    if key.lower() == name_lower:
                        component = prop.copy()
                        break
        else:
            # If still not found, create minimal schema
            component = {'type': 'string'}
            # Add date-time format for date fields
            if any(date_indicator in name.lower() for date_indicator in ['datum', 'zeit', 'beginn', 'ende']):
                component['format'] = 'date-time'
    
    # Add EDIFACT mapping to description if available
    if current_path in edifact_mappings and edifact_mappings[current_path]:
        if 'description' not in component:
            component['description'] = ''
        if component['description']:
            component['description'] += ' | '
        component['description'] += f"EDIFACT: {edifact_mappings[current_path]}"
    
    # Get the component and resolve all references
    resolved = resolve_schema_refs(component, base_schema)
    # Simplify boTyp enums and remove examples
    simplified = simplify_bo_typ(resolved)
    # Filter properties based on CSV paths
    filtered = filter_properties(simplified, required_paths)
    
    return filtered

def extract_nested_path(path: str) -> List[Tuple[str, bool]]:
    """Extract nested path components and whether they are arrays."""
    components = []
    current = ""
    is_array = False
    
    for char in path:
        if char == '.':
            if current:
                components.append((current, is_array))
                current = ""
                is_array = False
        elif char == '[' and current:
            is_array = True
        elif char == ']':
            continue
        else:
            current += char
    
    if current:
        components.append((current, is_array))
    
    return components

def add_nested_property(schema: Dict[str, Any], path_components: List[Tuple[str, bool]], base_schema: Dict[str, Any], required_paths: Set[str], edifact_mappings: Dict[str, str], current_path: str) -> None:
    """Add a nested property to the schema based on path components."""
    if not path_components:
        return
    
    current_comp, is_array = path_components[0]
    remaining = path_components[1:]
    
    if 'properties' not in schema:
        schema['properties'] = {}
    
    # Update current path for EDIFACT mapping
    new_path = f"{current_path}.{current_comp}"
    if is_array:
        new_path += "[]"
    
    if current_comp not in schema['properties']:
        if is_array:
            array_schema = {
                'type': 'array',
                'items': {'type': 'object', 'properties': {}}
            }
            if remaining:
                add_nested_property(array_schema['items'], remaining, base_schema, required_paths, edifact_mappings, new_path)
            else:
                # Try to find component in base schema
                comp_schema = get_schema_component(current_comp.split('[')[0], base_schema, required_paths, edifact_mappings, new_path)
                if comp_schema:
                    array_schema['items'] = comp_schema
            schema['properties'][current_comp] = array_schema
        else:
            if remaining:
                obj_schema = {'type': 'object', 'properties': {}}
                add_nested_property(obj_schema, remaining, base_schema, required_paths, edifact_mappings, new_path)
                schema['properties'][current_comp] = obj_schema
            else:
                comp_schema = get_schema_component(current_comp, base_schema, required_paths, edifact_mappings, new_path)
                if comp_schema:
                    schema['properties'][current_comp] = comp_schema
    else:
        target = schema['properties'][current_comp]
        if is_array and 'type' in target and target['type'] == 'array':
            target = target['items']
        if remaining:
            add_nested_property(target, remaining, base_schema, required_paths, edifact_mappings, new_path)

def create_schema_structure(base_schema: Dict[str, Any], required_paths: Set[str], edifact_mappings: Dict[str, str]) -> Dict[str, Any]:
    """Create the complete schema structure dynamically from CSV paths."""
    # Extract top-level components from paths
    components = extract_components_from_paths(required_paths)
    
    # Build properties for each top-level section
    properties = {}
    for top_level, comps in components.items():
        top_level_props = {}
        
        # Process each path that starts with this top_level
        for path in required_paths:
            if path.startswith(top_level + '.'):
                # Extract nested path components
                nested_path = path[len(top_level)+1:]  # Remove top_level and dot
                path_components = extract_nested_path(nested_path)
                
                # Add nested properties to the schema
                if path_components:
                    if top_level not in properties:
                        properties[top_level] = {'type': 'object', 'properties': {}}
                    add_nested_property(properties[top_level], path_components, base_schema, required_paths, edifact_mappings, top_level)
    
    # Create the final schema
    schema = {
        'type': 'object',
        'properties': properties
    }
    
    # Add required fields if they exist in the paths
    if components:
        schema['required'] = list(components.keys())
    
    return schema

def resolve_ref(ref: str, all_schemas: Dict[str, Any], resolved_refs: Set[str], ref_path: List[str]) -> Optional[Dict[str, Any]]:
    """Resolve a single $ref reference."""
    if ref.startswith('#/components/schemas/'):
        ref_name = ref.split('/')[-1]
        
        # Check for circular reference
        if ref_name in ref_path:
            print(f"Circular reference detected: {' -> '.join(ref_path)} -> {ref_name}")
            return {'type': 'object', 'description': f'Circular reference to {ref_name}'}
        
        if ref_name in all_schemas:
            resolved_refs.add(ref_name)
            schema_copy = copy.deepcopy(all_schemas[ref_name])
            return schema_copy
    return None

def simplify_bo_typ(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Simplify boTyp enum to only include the default value if present."""
    if not isinstance(schema, dict):
        return schema
    
    # Create a new dict to avoid modifying while iterating
    result = {}
    
    for key, value in schema.items():
        if key == 'example' and isinstance(value, dict) and '$ref' in value:
            # Skip example fields that contain $ref
            continue
        elif key == 'boTyp' and isinstance(value, dict):
            # If there's a default value, use only that in the enum
            if 'default' in value:
                default_value = value['default']
                result[key] = {
                    'title': value.get('title', 'BOTyp'),
                    'type': 'string',
                    'description': value.get('description', 'Typ des BO'),
                    'enum': [default_value]
                }
            else:
                result[key] = value
        elif isinstance(value, dict):
            result[key] = simplify_bo_typ(value)
        elif isinstance(value, list):
            result[key] = [simplify_bo_typ(item) if isinstance(item, dict) else item for item in value]
        else:
            result[key] = value
    
    return result

def normalize_path(path: str) -> str:
    """Normalize a path by converting array notation and lowercase."""
    # Replace array notation with a special marker
    path = path.replace('[]', '.items')
    return path.lower()

def is_path_match(path: str, csv_path: str) -> bool:
    """Check if a schema path matches a CSV path."""
    schema_path = normalize_path(path)
    csv_path = normalize_path(csv_path)
    
    # Split paths into components
    schema_parts = schema_path.split('.')
    csv_parts = csv_path.split('.')
    
    # Check if schema path is a prefix of csv path
    return len(schema_parts) <= len(csv_parts) and all(
        s == c for s, c in zip(schema_parts, csv_parts)
    )

def filter_properties(schema: Dict[str, Any], required_paths: Set[str], current_path: str = '') -> Dict[str, Any]:
    """Filter properties based on CSV paths and required fields."""
    if not isinstance(schema, dict):
        return schema

    result = {}
    
    # Always keep type, title, description
    for key in ['type', 'title', 'description']:
        if key in schema:
            result[key] = schema[key]
    
    # Handle arrays
    if schema.get('type') == 'array' and 'items' in schema:
        result['type'] = 'array'
        result['items'] = filter_properties(schema['items'], required_paths, f"{current_path}.items")
        return result
    
    # Handle properties
    if 'properties' in schema:
        filtered_props = {}
        required_fields = schema.get('required', [])
        
        for prop_name, prop_value in schema['properties'].items():
            prop_path = f"{current_path}.{prop_name}" if current_path else prop_name
            
            # A property should be kept if:
            # 1. It's required OR
            # 2. It matches (or is a parent of) a CSV path
            is_required = prop_name in required_fields
            matches_path = any(is_path_match(prop_path, csv_path) for csv_path in required_paths)
            
            if is_required or matches_path:
                filtered_props[prop_name] = filter_properties(prop_value, required_paths, prop_path)
        
        if filtered_props:
            result['properties'] = filtered_props
            if required_fields:
                result['required'] = [f for f in required_fields if f in filtered_props]
    
    # Handle nested objects
    elif isinstance(schema, dict):
        for key, value in schema.items():
            if key not in result:  # Skip already processed keys
                if isinstance(value, (dict, list)):
                    filtered = filter_properties(value, required_paths, f"{current_path}.{key}")
                    if filtered:
                        result[key] = filtered
                else:
                    result[key] = value
    
    return result

def resolve_schema_refs(schema: Dict[str, Any], all_schemas: Dict[str, Any], resolved_refs: Optional[Set[str]] = None, ref_path: Optional[List[str]] = None) -> Dict[str, Any]:
    """Recursively resolve all $ref references in the schema."""
    if resolved_refs is None:
        resolved_refs = set()
    if ref_path is None:
        ref_path = []
    
    if not isinstance(schema, dict):
        return schema
    
    resolved = {}
    for key, value in schema.items():
        if key == '$ref' and isinstance(value, str):
            ref_schema = resolve_ref(value, all_schemas, resolved_refs, ref_path)
            if ref_schema:
                # Get the schema name from the ref
                ref_name = value.split('/')[-1]
                # Add it to the reference path before resolving nested refs
                new_ref_path = ref_path + [ref_name]
                # Recursively resolve any refs in the referenced schema
                resolved_ref = resolve_schema_refs(ref_schema, all_schemas, resolved_refs, new_ref_path)
                resolved.update(resolved_ref)
            else:
                resolved[key] = value
        elif isinstance(value, dict):
            resolved[key] = resolve_schema_refs(value, all_schemas, resolved_refs, ref_path)
        elif isinstance(value, list):
            resolved[key] = [
                resolve_schema_refs(item, all_schemas, resolved_refs.copy(), ref_path.copy()) 
                if isinstance(item, dict) else item 
                for item in value
            ]
        else:
            resolved[key] = value
    
    return resolved

def load_process_info(json_file: str) -> Dict[str, Dict[str, str]]:
    """Load process info from JSON file and create a mapping of pruefidentifikator to process details."""
    with open(json_file, 'r', encoding='utf-8') as f:
        process_info = json.load(f)
    
    # Create a mapping of pruefidentifikator to process details
    process_map = {}
    for entry in process_info:
        if entry.get('pruefidentifikator'):
            process_map[entry['pruefidentifikator']] = {
                'absender': entry.get('absender', ''),
                'empfaenger': entry.get('empfaenger', ''),
                'aktion': entry.get('aktion', '')
            }
    return process_map

def add_process_descriptions(schema: Dict[str, Any], process_map: Dict[str, Dict[str, str]], pruefidentifikator: str) -> None:
    """Add description to schema based on process info."""
    if not pruefidentifikator or pruefidentifikator not in process_map:
        return
        
    process = process_map[pruefidentifikator]
    description = f"{pruefidentifikator} - {process['absender']} an {process['empfaenger']} - {process['aktion']}"
    
    # Add description only at the root level
    schema['description'] = description

def main():
    """Main function to generate the schema."""
    csv_file = "55002.csv"
    output_file = "55002.yaml"
    pruefidentifikator = "55002"
    process_info_file = "../processinfo.json"
    
    # Load required paths and EDIFACT mappings from CSV
    required_paths, edifact_mappings = load_csv_paths(csv_file)
    
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

if __name__ == "__main__":
    main()
