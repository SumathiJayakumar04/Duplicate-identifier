import os
import json

def categorize_files(folder_path, rules_file='rules.json'):
    try:
        with open(rules_file, 'r') as f:
            rules = json.load(f)
    except FileNotFoundError:
        print("❌ rules.json not found.")
        return {}

    categorized = {category: [] for category in rules}

    for root, _, files in os.walk(folder_path):
        for file in files:
            ext = file.split('.')[-1].lower()
            full_path = os.path.join(root, file)
            for category, extensions in rules.items():
                if ext in extensions:
                    categorized[category].append(full_path)
                    break  # Avoid multiple category matches

    return categorized
