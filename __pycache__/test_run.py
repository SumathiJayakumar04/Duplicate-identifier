from duplicate_finder import find_duplicates

folder_path = input("📁 Enter the folder path to scan: ")
duplicates = find_duplicates(folder_path)

if duplicates:
    print("\n🟠 Duplicates found:")
    for dup in duplicates:
        print("  -", dup)
else:
    print("\n✅ No duplicates found.")
