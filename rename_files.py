#!/usr/bin/env python3
import os
import sys
import shutil

def replace_file_content(file_path, replacements):
    """Replace text patterns in file content."""
    try:
        # Check if file is binary
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            print(f"Skipping binary file: {file_path}")
            return

        # Perform replacements
        new_content = content
        for old, new in replacements:
            if old in new_content:
                new_content = new_content.replace(old, new)

        # Only write if content has changed
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated content in: {file_path}")
    except Exception as e:
        print(f"Error processing file content {file_path}: {str(e)}")

def rename_files(directory):
    """Rename files and directories containing the patterns and update their content."""
    replacements = [
        ('fastgpt', 'libchat'),
        ('FastGPT', 'LibChat'),
        ('FASTGPT', 'LIBCHAT')
    ]
    
    # Walk bottom-up to handle directories properly
    for root, dirs, files in os.walk(directory, topdown=False):
        # Process file contents and rename files
        for old_name in files:
            # First replace content in the file
            file_path = os.path.join(root, old_name)
            replace_file_content(file_path, replacements)
            
            # Then rename the file if needed
            new_name = old_name
            for old, new in replacements:
                if old in new_name:
                    new_name = new_name.replace(old, new)
            
            if new_name != old_name:
                old_path = os.path.join(root, old_name)
                new_path = os.path.join(root, new_name)
                try:
                    shutil.move(old_path, new_path)
                    print(f"Renamed file: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming {old_path}: {str(e)}")
        
        # Rename directories
        for old_name in dirs:
            new_name = old_name
            for old, new in replacements:
                if old in new_name:
                    new_name = new_name.replace(old, new)
            
            if new_name != old_name:
                old_path = os.path.join(root, old_name)
                new_path = os.path.join(root, new_name)
                try:
                    shutil.move(old_path, new_path)
                    print(f"Renamed directory: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming {old_path}: {str(e)}")

def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python rename_files.py <directory>")
            sys.exit(1)
            
        target_dir = sys.argv[1]
        if not os.path.isdir(target_dir):
            print(f"Error: {target_dir} is not a directory")
            sys.exit(1)
            
        # Change to target directory
        os.chdir(target_dir)
        
        # Rename files and directories
        print("\nRenaming files and directories...")
        rename_files('.')
        
        print("\nRename operation completed successfully!")
                    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 