import os
import yaml

def sort_yaml_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = yaml.safe_load(file)
            
            if isinstance(data, list):
                data.sort()
                with open(filepath, 'w') as file:
                    yaml.dump(data, file, default_flow_style=False)
            elif isinstance(data, dict):
                sorted_data = {k: data[k] for k in sorted(data)}
                with open(filepath, 'w') as file:
                    yaml.dump(sorted_data, file, default_flow_style=False)

if __name__ == "__main__":
    directory = "macoapp-schreiben/components/examples/Strom"
    sort_yaml_files(directory)