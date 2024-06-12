import os
import json
import glob
import re
from pathlib import Path

# Regular expression pattern to identify and remove download button lines
download_pattern = re.compile(
    r"- \[Download Jupyter Notebook\]\(\.\./code/.*\.ipynb\)\{download=\".*\.ipynb\"\}"
)

# CONVERT
# Convert files from .qmd to .ipynb
for i in glob.iglob('python/*.qmd'):
    os.system(f"quarto convert {i}")

# MOVE FILES
source_folder = Path('python/')
destination_folder = Path('code/')
# Loop through all .ipynb files in the source folder
for filepath in source_folder.glob('*.ipynb'):
    # Construct the destination path
    destination = destination_folder / filepath.name
    # Move the file
    filepath.rename(destination)

# JUPYTER NOTEBOOKS ADJUSTMENT

# Folder containing the .ipynb files
folder_path = Path('code/')

# Loop through all .ipynb files in the folder
for file_path in folder_path.glob('*.ipynb'):
    with file_path.open('r', encoding='utf-8') as file:
        notebook_content = json.load(file)

    # Process markdown cells and remove unwanted download button string
    for cell in notebook_content['cells']:
        if cell['cell_type'] == 'markdown':
            cell['source'] = [
                line for line in cell['source']
                if not download_pattern.search(line)
            ]

    # Process code cells to remove comments starting with "# |"
    for cell in notebook_content['cells']:
        if cell['cell_type'] == 'code':
            cell['source'] = [
                line for line in cell['source']
                if not line.strip().startswith("# |")
            ]

    # Find and remove the first raw cell if it exists
    for index, cell in enumerate(notebook_content['cells']):
        if cell['cell_type'] == 'raw':
            del notebook_content['cells'][index]
            break

    # Find and remove the last markdown cell
    for index in reversed(range(len(notebook_content['cells']))):
        if notebook_content['cells'][index]['cell_type'] == 'markdown':
            del notebook_content['cells'][index]
            break

    # Write the modified content back to the file
    with file_path.open('w', encoding='utf-8') as file:
        json.dump(notebook_content, file, ensure_ascii=False, indent=4)
