Duplicate File Finder & Organizer
📌 Overview

This project is a Python-based GUI application that detects duplicate files based on their content and helps users manage storage efficiently. It also provides features to delete duplicate files and organize files into categories automatically.

🚀 Features
🔍 Content-Based Duplicate Detection using SHA-256 hashing
📁 Recursive Folder Scanning to detect duplicates in subdirectories
⚡ Multithreading Support for faster processing without UI freeze
🗑️ Safe Duplicate Deletion with confirmation prompts
🧩 Automatic File Categorization based on file extensions
🖥️ User-Friendly GUI built with Tkinter and ttkbootstrap
🛠️ Tech Stack
Language: Python
Libraries:
os – file handling and directory traversal
hashlib – generating SHA-256 hashes
threading – background processing
tkinter – GUI development
ttkbootstrap – modern UI styling
⚙️ How It Works
Select a folder using the GUI
The system scans all files using os.walk()
Each file is hashed using SHA-256
Files with identical hashes are identified as duplicates
Duplicate files are displayed in the interface
Users can delete selected duplicates or organize files
📸 Application Workflow
Select Folder
Find Duplicates
View Duplicate Files
Delete or Categorize Files
