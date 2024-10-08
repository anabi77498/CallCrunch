import os
import json
from anthropic import Anthropic

# Set up the Anthropic client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def list_files_in_directory():
    # Define the list of files and directories to ignore
    files_to_ignore = ['venv', '.gitignore', '.env', '__pycache__', '.git', 'data', 'claude.py', 'test.ipynb', 'README.md']
    
    root_dir = os.path.abspath(os.curdir)  # Get the current directory (root directory)
    all_files = []
    
    # Walk through the root directory
    for root, dirs, files in os.walk(root_dir):
        # Modify the dirs in-place to remove any directories we want to ignore
        dirs[:] = [d for d in dirs if d not in files_to_ignore]

        # For each file found, store the path relative to the root directory, unless it's in the ignore list
        for file in files:
            if file not in files_to_ignore:
                relative_path = os.path.relpath(os.path.join(root, file), root_dir)
                all_files.append(relative_path)
    
    return all_files

def pull_file_contents(files):

    file_contents = []
    
    # Loop through all files and print their content
    for file_path in files:
        info = f"=== {file_path} ==="
        print(f"=== {file_path} ===")
        
        # Open and print the file contents
        try:
            with open(file_path, 'r') as file:
                # print(file.read())
                data = file.read()
                info += "\n" 
                info += data
        except Exception as e:
            print(f"Could not read file {file_path}: {e}")
        
        file_contents.append(info)

    return file_contents

def identify_necessary_files(file_structure, task):
    """Ask Claude to identify necessary files for the task."""
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": (
                    "Here's the file structure of the repository:\n"
                    f"{file_structure}\n\n"
                    f"Task: {task}\n\n"
                    "Please update the file and code to solve the following task"
                )
            }
        ]
    )
    # Extract and return the JSON response containing necessary file paths
    return json.loads(message.messages[0]["content"])

def modify_files(file_info, task):
    """Ask Claude to modify the necessary files to achieve the task."""
    results = {}
    

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Here's the content of my repository: \n {file_info}"
                    f"Task: {task}\n\n"
                    "Please modify the files to achieve the task. Provide the entire updated content."
                )
            }
        ]
    )

    # Store the updated file content returned by Claude
    results = message.messages[0]["content"]

    return results

# Get the list of files from the repository
file_information = list_files_in_directory()

files_data = pull_file_contents(file_information)
print(files_data)

file_structure = "\n".join(files_data)

# Define your task
task = "Add a new endpoint to the backend with the route '/hello' that prints hello"

# Identify the necessary files
file_structure = "\n\n".join(files_data)

with open('claude_input.txt', 'w') as file:
    # Write the string to the file
    file.write(file_structure)

if file_structure:
    updated_files = modify_files(file_structure, task)

    # Output the updated files and their new contents
    print(f"=== Updated Repository ===")
    print(updated_files)
    print("\n")
else:
    print("No files were identified as necessary for the task.")
