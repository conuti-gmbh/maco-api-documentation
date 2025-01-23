import os
import yaml

def find_yml_without_description(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".yml"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as yml_file:
                    try:
                        content = yaml.safe_load(yml_file)
                        if 'description' not in content:
                            print(file_path)
                            content['description'] = file.replace('.yml', '')
                            with open(file_path, 'w') as yml_file_write:
                                yaml.safe_dump(content, yml_file_write)
                    except yaml.YAMLError as exc:
                        print(f"Error parsing {file_path}: {exc}")

if __name__ == "__main__":
    directory = "/home/lena/projekts/maco-api-documentation/macoapp-schreiben/components/requestBodies/PIs"
    find_yml_without_description(directory)
