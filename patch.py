#!/usr/bin/env python3
import os
import re
import sys

def read_public_key():
    with open('/tmp/public.pem', 'r') as f:
        return f.read().strip()

def replace_in_file(file_path, new_key):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace public key if present
        if 'BEGIN PUBLIC KEY' in content:
            print(f"Found key in: {file_path}")
            pattern = r'd\s*=\s*`-----BEGIN PUBLIC KEY-----[^`]*-----END PUBLIC KEY-----`'
            content = re.sub(pattern, f'd = `{new_key}`', content)
            print(f"Replaced key in: {file_path}")
        
        # Replace text patterns
        replacements = [
            ('fastgpt', 'libchat'),
            ('FastGPT', 'LibChat'),
            ('FASTGPT', 'LIBCHAT')
        ]
        
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                print(f"Replaced '{old}' with '{new}' in: {file_path}")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def rename_files(directory):
    """Rename files and directories containing the patterns."""
    replacements = [
        ('fastgpt', 'libchat'),
        ('FastGPT', 'LibChat'),
        ('FASTGPT', 'LIBCHAT')
    ]
    
    # Walk bottom-up to handle directories properly
    for root, dirs, files in os.walk(directory, topdown=False):
        # Rename files
        for old_name in files:
            new_name = old_name
            for old, new in replacements:
                if old in new_name:
                    new_name = new_name.replace(old, new)
            
            if new_name != old_name:
                old_path = os.path.join(root, old_name)
                new_path = os.path.join(root, new_name)
                try:
                    os.rename(old_path, new_path)
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
                    os.rename(old_path, new_path)
                    print(f"Renamed directory: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming {old_path}: {str(e)}")

def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python patch.py <directory>")
            sys.exit(1)
            
        target_dir = sys.argv[1]
        if not os.path.isdir(target_dir):
            print(f"Error: {target_dir} is not a directory")
            sys.exit(1)
            
        # Change to target directory
        os.chdir(target_dir)
        
        # Read the new public key
        new_key = read_public_key()
        print("Read new public key successfully")

        # First replace content in files
        for root, _, files in os.walk('.'):
            for file in files:
                file_path = os.path.join(root, file)
                replace_in_file(file_path, new_key)
        
        # Then rename files and directories
        rename_files('.')
                    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 