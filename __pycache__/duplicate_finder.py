import os
import hashlib

# Calculates the SHA-256 hash of a file
def calculate_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Finds duplicate files in the folder by comparing hashes
def find_duplicates(folder_path):
    hash_map = {}
    duplicates = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                file_hash = calculate_hash(filepath)
                if file_hash in hash_map:
                    duplicates.append(filepath)  # It's a duplicate
                else:
                    hash_map[file_hash] = filepath
            except Exception as e:
                print(f"❌ Error reading file {filepath}: {e}")
    
    return duplicates

