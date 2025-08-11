import os
import hashlib

def calculate_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def find_duplicates(folder_path):
    hash_map = {}
    duplicates = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                file_hash = calculate_hash(filepath)
                if file_hash in hash_map:
                    duplicates.append(filepath)
                else:
                    hash_map[file_hash] = filepath
            except Exception as e:
                print(f"Error reading file {filepath}: {e}")
    return duplicates
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)

def scan_for_duplicates():
    folder = folder_path.get()
    if not os.path.isdir(folder):
        messagebox.showerror("Error", "Invalid folder path")
        return
    
    duplicates = find_duplicates(folder)
    result_list.delete(0, tk.END)
    if duplicates:
        for dup in duplicates:
            result_list.insert(tk.END, dup)
        messagebox.showinfo("Result", f"{len(duplicates)} duplicates found.")
    else:
        messagebox.showinfo("Result", "No duplicates found.")

root = tk.Tk()
root.title("JP-001: Duplicate Finder")

folder_path = tk.StringVar()

tk.Label(root, text="Select Folder").pack()
tk.Entry(root, textvariable=folder_path, width=50).pack()
tk.Button(root, text="Browse", command=browse_folder).pack()
tk.Button(root, text="Scan", command=scan_for_duplicates).pack()

result_list = Listbox(root, width=80, height=10)
result_list.pack()

root.mainloop()
def delete_selected():
    selected = result_list.curselection()
    if not selected:
        messagebox.showwarning("Warning", "No file selected")
        return
    
    for i in reversed(selected):
        filepath = result_list.get(i)
        try:
            os.remove(filepath)
            result_list.delete(i)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete {filepath}\n{e}")

tk.Button(root, text="Delete Selected", command=delete_selected).pack()
import json
import shutil

def load_rules():
    with open("rules.json", "r") as f:
        return json.load(f)

def categorize_files(folder):
    rules = load_rules()
    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        if not os.path.isfile(filepath):
            continue
        for rule in rules:
            for keyword in rule["keywords"]:
                if keyword.lower() in file.lower():
                    category_folder = os.path.join(folder, rule["category"])
                    os.makedirs(category_folder, exist_ok=True)
                    shutil.move(filepath, os.path.join(category_folder, file))
                    break
tk.Button(root, text="Categorize Files", command=lambda: categorize_files(folder_path.get())).pack()
