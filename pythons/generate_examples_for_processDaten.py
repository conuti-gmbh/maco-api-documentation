import json
import os

# This script generates output from a JSON file, removes duplicates by 'pruefidentifikator',
# sorts the data, and writes the output to a YAML file.
# To run this script, use the command: python generate_examples_for_processDaten.py

def generate_output_from_json(file_path):
    # Load the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Remove duplicates by pruefidentifikator
    unique_data = {element['pruefidentifikator']: element for element in data}.values()
    
    # Sort the data by pruefidentifikator
    sorted_data = sorted(unique_data, key=lambda x: x['pruefidentifikator'])
    
    # Open the output file in write mode
    with open('../macoapp-schreiben/commands/PROZESSDATEN/EXAMPLES.yaml', 'w') as output_file:
        # Loop through each element in the sorted array and generate the required output
        for element in sorted_data:
            pruefidentifikator = element['pruefidentifikator']
            empfaenger = element['empfaenger']
            aktion = element['aktion'].replace('\n', '').replace('\t', '')
            
            # Check if any of the Testfall files exist
            testfall_paths = [
                f"../macoapp-schreiben/components/examples/Strom/{pruefidentifikator}_eingehend_Testfall1.yaml",
                f"../macoapp-schreiben/components/examples/Strom/{pruefidentifikator}_eingehend_Testfall2.yaml",
                f"../macoapp-schreiben/components/examples/Strom/{pruefidentifikator}_eingehend_Testfall3.yaml",
                f"../macoapp-schreiben/components/examples/Strom/{pruefidentifikator}_eingehend_Testfall4.yaml"
            ]
            
            if not any(os.path.exists(path) for path in testfall_paths):
                print(f"Not found examples for: {pruefidentifikator}")
                continue
            
            output = f"\"PI {pruefidentifikator} - ROLLE {empfaenger} : {aktion}\""
            output_file.write(output + '\n')
            for i in range(1, 3):  # Generate paths for Testfall1 and Testfall2
                for ext in ['yml', 'yaml']:
                    if os.path.exists(f"../macoapp-schreiben/components/examples/Strom/{pruefidentifikator}_eingehend_Testfall{i}.{ext}"):
                        output = f"  $ref: ../../components/examples/Strom/{pruefidentifikator}_eingehend_Testfall{i}.{ext}"
                        output_file.write(output + '\n')

# Call the function with the path to the JSON file
generate_output_from_json('processinfo.json')
