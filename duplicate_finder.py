import os
import hashlib
from collections import defaultdict

def calculate_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def find_duplicates(folder_path):
    size_map = defaultdict(list)
    duplicates = {}

    # Step 1: Group files by size
    for root, _, files in os.walk(folder_path):
        for file in files:
            path = os.path.join(root, file)
            try:
                size = os.path.getsize(path)
                size_map[size].append(path)
            except Exception as e:
                print(f"Error: {e}")

    # Step 2: Within same-size groups, compare hashes
    for size_group in size_map.values():
        if len(size_group) < 2:
            continue
        hash_map = {}
        for file_path in size_group:
            try:
                file_hash = calculate_hash(file_path)
                if file_hash in hash_map:
                    duplicates.setdefault(file_hash, [hash_map[file_hash]])
                    duplicates[file_hash].append(file_path)
                else:
                    hash_map[file_hash] = file_path
            except Exception as e:
                print(f"Error hashing {file_path}: {e}")

    # Flatten the duplicate groups
    result = []
    for group in duplicates.values():
        result.extend(group)
    return result
