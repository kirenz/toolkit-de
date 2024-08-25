import os
import re

# Directories
input_directory = 'github'
output_directory = 'slides'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# YAML front matter template
yml_template = '''---
title: {title}
lang: de
subtitle: Subtitle
author: Jan Kirenz
execute:
  eval: false
  echo: true
highlight-style: github-dark
format:
  revealjs: 
    toc: false
    toc-depth: 1
    embed-resources: false
    theme: [default, /style/custom.scss]
    incremental: true
    transition: slide
    background-transition: fade
    transition-speed: slow
    code-copy: true
    code-line-numbers: true
    smaller: false
    scrollable: true
    slide-number: c
    preview-links: auto
    css: /style/index.css
    chalkboard: 
      buttons: false
    logo: images/logo.png
    footer: {title} | Jan Kirenz
jupyter: python3
---
'''

# Process each .qmd file in the input directory
for file_name in os.listdir(input_directory):
    if file_name.endswith('.qmd'):
        input_path = os.path.join(input_directory, file_name)

        # Read the file contents
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.readlines()

        # Extract the first headline to use as the title
        title = None
        updated_content = []
        for line in content:
            if line.startswith('# ') and title is None:
                title = line[2:].strip()
            elif line.startswith('###') or line.startswith('####'):
                updated_content.append('##' + line[3:])
            else:
                updated_content.append(line)

        # Ensure a title was found
        if title is None:
            print(f'Warning: No top-level headline found in {file_name}, skipping this file.')
            continue

        # Create the new YAML content
        new_yml = yml_template.format(title=title)
        new_content = new_yml + '\n' + ''.join(updated_content)

        # Write the new content to the output directory
        output_file_name = os.path.splitext(file_name)[0] + '.qmd'
        output_path = os.path.join(output_directory, output_file_name)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f'Processed {file_name} into {output_file_name}')
