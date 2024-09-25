import os

def write_index_file(directory, output_file):
    """
    Writes a list of all .yml files in the specified directory to an index file.

    Args:
        directory (str): Directory to list .yml files from.
        output_file (str): Path to the output index file.
    """
    # Get a list of all .yml files in the directory
    yml_files = [f for f in os.listdir(directory) if f.endswith('.yml')]

    # Write the list of files to the index file
    with open(output_file, 'w') as f:
        for yml_file in yml_files:
            # Remove the .yml extension from the filename
            filename = yml_file[:-4]
            # Write the entry to the index file
            f.write(f"/{filename}:\n")
            f.write(f"  $ref: {yml_file}\n\n")

if __name__ == "__main__":
    directory = "paths"
    output_file = "1.index.yml"
    write_index_file(directory, output_file)
