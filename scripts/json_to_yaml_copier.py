import json
import yaml
import os

src_dir = 'maco-edi-testfiles/inbound/v202404/UTILMD/Strom/'
dst_dir = 'bo4e/components/examples/Strom/'

if not os.path.exists(src_dir):
    print(f"Source directory '{src_dir}' does not exist.")
    exit(1)

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

for filename in os.listdir(src_dir):
    if filename.endswith('.json'):
        src_file = os.path.join(src_dir, filename)
        dst_file = os.path.join(dst_dir, filename.replace('.json', '.yaml'))

        with open(src_file, 'r') as json_file:
            data = json.load(json_file)

        value = data.get('data')

        yaml_data = {'value': value}

        with open(dst_file, 'w') as yaml_file:
            yaml.dump(yaml_data, yaml_file, default_flow_style=False)

        print(f"Copied and converted '{src_file}' to '{dst_file}'")
