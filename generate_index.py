#!/usr/bin/env python3

"""
generate_index.py - Generate an index of Markdown files in a directory.

Instructions on how to run the script:

    python3 generate_index.py

Run this command in the root directory of your project.

This script traverses the 'docs/' directory up to a maximum depth and generates an 'index-contents.md' file listing the Markdown files found. It sorts the files based on the display name, ignoring specified prefixes ('The ', 'Work with ') when sorting. Specified directories are excluded from the index, except that 'release-notes.md' from the 'release-notes' directory is included. The '404.md' file is ignored.

"""

import os

def strip_prefixes(s):
    prefixes = ('The ', 'Work with ')
    s_lower = s.lower()
    for prefix in prefixes:
        if s_lower.startswith(prefix.lower()):
            return s[len(prefix):]
    return s

# Define the directory containing your Markdown files
docs_dir = os.path.join(os.getcwd(), 'docs')

# Path to the index-contents.md file
index_file_path = os.path.join(docs_dir, 'index-contents.md')

# Delete 'index-contents.md' if it exists
if os.path.exists(index_file_path):
    os.remove(index_file_path)
    print(f"Deleted existing index file: {index_file_path}")

# Prepare the content for index-contents.md
index_content = '# Index\n\n'

# Set the maximum depth (starting from 0)
max_depth = 5

# Directories to exclude from traversal
exclude_dirs = {'_static', 'assets', 'css', 'fonts', 'js', 'release-notes', 'release-notes/8.0'}

# Files to exclude
exclude_files = {'404.md', 'index-contents.md'}

# Calculate the length of the base path to measure depth
base_path_length = len(docs_dir.rstrip(os.sep).split(os.sep))

# Initialize a variable to track the previous directory path
previous_dir = ''

# Walk through the docs directory
for root, dirs, files in os.walk(docs_dir):
    # Exclude specified directories from traversal, but keep 'release-notes' to include 'release-notes.md'
    dirs[:] = [d for d in dirs if d not in exclude_dirs]

    # Calculate the current depth
    current_depth = len(root.rstrip(os.sep).split(os.sep)) - base_path_length

    # Limit the traversal to the maximum depth
    if current_depth >= max_depth:
        dirs.clear()
        continue

    # Sort the directories alphabetically
    dirs.sort()

    # Exclude non-Markdown files and specified files
    files = [f for f in files if f.endswith('.md') and f not in exclude_files]

    # Get the relative directory path from docs_dir
    relative_dir = os.path.relpath(root, docs_dir)
    relative_dir = relative_dir.replace(os.sep, '/')

    # Only add directory headings when the directory changes
    if relative_dir != previous_dir:
        # Add directories as headers except for the root 'docs' directory
        if relative_dir != '.':
            indent_level = relative_dir.count('/')
            indent = '  ' * indent_level

            # Modify directory display name
            dir_display_name_parts = relative_dir.split('/')
            dir_display_name_parts = [
                'Release notes' if part.lower() == 'release-notes' else part
                for part in dir_display_name_parts
            ]
            dir_display_name = '/'.join(dir_display_name_parts)

            # Remove bold formatting from directory names
            index_content += f'{indent}- {dir_display_name}/\n'
        previous_dir = relative_dir

    # Initialize a list to hold file entries with display names
    file_entries = []

    # Process files to extract display names
    for file in files:
        # Exclude '404.md' in any location
        if file == '404.md':
            continue

        filepath = os.path.join(root, file)
        relative_path = os.path.relpath(filepath, docs_dir)
        # Convert backslashes to slashes for cross-platform compatibility
        relative_path = relative_path.replace(os.sep, '/')

        directories_in_path = os.path.dirname(relative_path).split('/')

        if 'release-notes' in directories_in_path:
            # Include only 'release-notes.md' from 'release-notes' directory
            if file != 'release-notes.md':
                continue
        else:
            # Skip files in excluded directories
            if any(ex_dir in directories_in_path for ex_dir in exclude_dirs):
                continue

        # Extract the display name from the first level 1 heading or filename
        display_name = ''
        try:
            with open(filepath, 'r', encoding='utf-8') as md_file:
                for line in md_file:
                    if line.strip().startswith('# '):
                        display_name = line.strip()[2:].strip()
                        break
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            continue

        if not display_name:
            display_name = os.path.splitext(os.path.basename(file))[0]

        # For sorting, remove leading prefixes
        sort_key = strip_prefixes(display_name).strip().lower()
        # Append to the file_entries list
        file_entries.append((sort_key, display_name, relative_path))

    # Sort the file entries based on the adjusted display name (sort_key)
    file_entries.sort()

    # Indentation for files within directories
    for _, display_name, relative_path in file_entries:
        indent_level = relative_path.count('/') - 1
        indent = '  ' * indent_level
        index_content += f'{indent}  - [{display_name}]({relative_path})\n'

# Write the index-contents.md file in the 'docs' directory
with open(index_file_path, 'w', encoding='utf-8') as index_file:
    index_file.write(index_content)

print(f"Index generated at {index_file_path}")
