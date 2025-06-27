#!/usr/bin/env python3
import os
import re
import sys
import mimetypes

ORIGINAL_KEY = """
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAuRKwyP8XRYcC8+H17Nrm
0XRa1yRx6CIFnXkg5csSwRka/6KarKXrLirOAeg6icKR69DuP9E4F4NHvYDF6NWl
hGd13vhOg2ABlYx5Mz6e97GPdyHGYtE8ivL9s/ZAjmOAmBntru21Cz2XmmoODW0A
ubuojJY5o1AExDZopeqFfiWLb9Xp1U3+fJfSSTcpwOWJyJbgzeXpe5l6PRMa/1u6
iXjzLmL+wn91EyZpqIB58ZX/89k7cS82iQdNJ14N/yd9GfggV+gXvHNW9SlLkPSm
XsScZ5CjHeejMRrozBpBTzPoYEBRHNtUUFJcTdHsmXx7m5f/9bzPxDV2wgQ1AjoZ
4wN1cqlqtEkz8iwOeDhadS6LQcms9mjiQ61lFFrZxRGWjLWF7AtQmZ5AsR6Rfy+s
uxHhD7WRZzuxz4A7QDZzwXIUnADCA2CDTApttt6O5x9Q8XoVGr01jS88wX+fVq3V
YHKhgblQh1XUqCBmeeMeK3J/7ipWriHRrhp0yG/m9CROZp8nzdl4pRkO0CKJXe4r
NXNQe93HY91bjP+gWHVLV8P3xk08VVrdE1SM4eQYCQg+8YOpD3DEWBTAtvdknayf
Hvg2QTVvOHHwcIlSCo26ZpXOOE/El/3ZspJ7bWwIMckeN0x9guLTpc2W4jE6dY83
RZ7iPiNjuE6X10nchsf2OzsCAwEAAQ==
-----END PUBLIC KEY-----
"""

def is_binary_file(file_path):
    """Check if a file is binary."""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        # If we can't determine the type, try to read it as text
        try:
            with open(file_path, 'tr') as f:
                f.read(1024)
            return False
        except:
            return True
    return not mime_type.startswith(('text/', 'application/json', 'application/javascript', 'application/xml'))

def read_public_key():
    with open('/tmp/public.pem', 'r') as f:
        return f.read().strip()

def replace_in_file(file_path, new_key):
    try:
        # Skip binary files
        if is_binary_file(file_path):
            print(f"Skipping binary file: {file_path}")
            return

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        # Replace public key if present, using exact match
        if 'BEGIN PUBLIC KEY' in content:
            print(f"Found key in: {file_path}")
            if ORIGINAL_KEY.strip() in content:
                content = content.replace(ORIGINAL_KEY.strip(), new_key.strip())
                print(f"Replaced key in: {file_path}")
            else:
                print(f"Warning: Found public key header but exact key not found in: {file_path}")
        
        # Only write if content has changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python replace_key.py <directory>")
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

        # Replace content in files
        print("\nProcessing file contents...")
        for root, _, files in os.walk('.'):
            for file in files:
                file_path = os.path.join(root, file)
                replace_in_file(file_path, new_key)
        
        print("\nKey replacement completed successfully!")
                    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 