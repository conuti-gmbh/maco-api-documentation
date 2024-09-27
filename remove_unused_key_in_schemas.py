import json
import os

def remove_keys(file_path):
    keys_to_remove = ['$schema', '$id', 'faker', '$comment']
    with open(file_path, 'r') as file:
        data = json.load(file)

    def recursive_remove_keys(data):
        if isinstance(data, dict):
            for key in keys_to_remove:
                data.pop(key, None)
            for value in data.values():
                recursive_remove_keys(value)
        elif isinstance(data, list):
            for item in data:
                recursive_remove_keys(item)

    recursive_remove_keys(data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    schemas_dir = 'components/schemas/'
    for root, dirs, files in os.walk(schemas_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                remove_keys(file_path)
                print(f"Removed keys from file: {file_path}")

if __name__ == '__main__':
    main()
