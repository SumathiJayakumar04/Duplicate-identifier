import tkinter as tk
from tkinter import ttk, filedialog, messagebox, END
from duplicate_finder import find_duplicates
from categorizer import categorize_files
import threading
import os

# 🎨 Color theme (Dark mode)
BG_COLOR = "#2b2b2b"
FG_COLOR = "#ffffff"
BUTTON_BG = "#4CAF50"
BUTTON_FG = "#ffffff"
HIGHLIGHT_BG = "#444"

class DuplicateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JP-001 | Duplicate File Finder")
        self.root.attributes('-fullscreen', True)  # 🔲 Fullscreen mode
        self.root.configure(bg=BG_COLOR)

        # Setup custom style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background=BUTTON_BG, foreground=BUTTON_FG, font=('Helvetica', 11), padding=6)
        style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=('Helvetica', 12))
        style.map("TButton", background=[('active', '#45a049')])

        # Folder selection frame
        top_frame = ttk.Frame(root, padding=10)
        top_frame.pack(fill='x')

        self.folder_label = ttk.Label(top_frame, text="📁 No folder selected")
        self.folder_label.pack(side='left', padx=(10, 10))

        self.select_button = ttk.Button(top_frame, text="Select Folder", command=self.select_folder)
        self.select_button.pack(side='right')

        # Action buttons
        button_frame = ttk.Frame(root, padding=10)
        button_frame.pack(fill='x')

        self.scan_button = ttk.Button(button_frame, text="Find Duplicates", command=self.scan_duplicates)
        self.scan_button.pack(side='left', padx=5)

        self.categorize_button = ttk.Button(button_frame, text="Categorize Files", command=self.categorize_files)
        self.categorize_button.pack(side='left', padx=5)

        self.delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack(side='left', padx=5)

        # Listbox and Scrollbar
        listbox_frame = ttk.Frame(root, padding=10)
        listbox_frame.pack(fill='both', expand=True)

        self.listbox = tk.Listbox(listbox_frame,
                                  bg=BG_COLOR,
                                  fg=FG_COLOR,
                                  selectbackground=HIGHLIGHT_BG,
                                  selectforeground="Green",
                                  font=('Courier', 11),
                                  width=140,
                                  height=35,
                                  selectmode=tk.MULTIPLE,
                                  borderwidth=0,
                                  relief=tk.FLAT)
        self.listbox.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.folder_path = ""
        self.duplicates = []

        # Exit instruction
        exit_label = ttk.Label(root, text="Press [Esc] to exit fullscreen")
        exit_label.pack(side='bottom', pady=5)

        # Bind ESC to exit fullscreen
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = folder
            self.folder_label.config(text=f"📁 {folder}")

    def scan_duplicates(self):
        if not self.folder_path:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return

        self.listbox.delete(0, END)
        self.listbox.insert(END, "🔎 Scanning for duplicates... Please wait.")
        self.root.update_idletasks()

        thread = threading.Thread(target=self._do_scan)
        thread.start()

    def _do_scan(self):
        hash_map = {}
        duplicates = {}

        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    from duplicate_finder import calculate_hash
                    file_hash = calculate_hash(filepath)
                    if file_hash in hash_map:
                        duplicates.setdefault(file_hash, [hash_map[file_hash]])
                        duplicates[file_hash].append(filepath)
                    else:
                        hash_map[file_hash] = filepath
                except Exception as e:
                    print(f"❌ Error reading file {filepath}: {e}")

        self.duplicates = []
        self.listbox.delete(0, END)
        if not duplicates:
            self.listbox.insert(END, "✅ No duplicates found.")
        else:
            group_num = 1
            for group in duplicates.values():
                self.listbox.insert(END, f"🔁 Duplicate Group {group_num}:")
                for f in group:
                    self.listbox.insert(END, f)
                    self.duplicates.append(f)
                self.listbox.insert(END, "")
                group_num += 1

    def delete_selected(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("Info", "Please select files to delete.")
            return

        deleted_files = 0
        for i in reversed(selected):
            file_path = self.listbox.get(i)
            if file_path.startswith("🔁") or file_path.strip() == "":
                continue
            try:
                os.remove(file_path)
                self.listbox.delete(i)
                deleted_files += 1
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete {file_path}: {e}")

        if deleted_files:
            messagebox.showinfo("Deleted", f"{deleted_files} files deleted.")

    def categorize_files(self):
        if not self.folder_path:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return

        result = categorize_files(self.folder_path)
        if not result:
            messagebox.showinfo("Info", "No categories found or rules.json missing.")
            return

        self.listbox.delete(0, END)
        self.listbox.insert(END, "📂 Categorized Files:")
        for category, files in result.items():
            self.listbox.insert(END, f"\n📁 {category}")
            for f in files:
                self.listbox.insert(END, f"   - {f}")

# 🔁 Launch app
if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateApp(root)
    root.mainloop()


#python3 jp001_gui.py