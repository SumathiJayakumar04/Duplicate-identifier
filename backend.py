
import os
import hashlib

class Api:
    def calculate_hash(self, path):
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def find_duplicates(self, folder_path):
        hash_map = {}
        duplicates = {}

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    file_hash = self.calculate_hash(filepath)
                    if file_hash in hash_map:
                        duplicates.setdefault(file_hash, [hash_map[file_hash]])
                        duplicates[file_hash].append(filepath)
                    else:
                        hash_map[file_hash] = filepath
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

        result = []
        for group in duplicates.values():
            result.append(group)
        return result
