import tkinter as tk
from tkinter import filedialog, messagebox

def select_source_dir():
    source_dir = filedialog.askdirectory()
    if source_dir:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, source_dir)

def select_target_dir():
    target_dir = filedialog.askdirectory()
    if target_dir:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, target_dir)

def backup():
    source = source_entry.get()
    target = target_entry.get()
    if not source or not target:
        messagebox.showerror("Error", "Both source and target directories must be selected!")
    else:
        messagebox.showinfo("Info", "Backup initiated from {} to {}".format(source, target))
        # Add backup logic here

def full_backup():
    backup()
    # Add full backup logic here

def incremental_backup():
    backup()
    # Add incremental backup logic here

# Create the main window
root = tk.Tk()
root.title("Backup Tool")
root.geometry("500x300")

# Title
title_label = tk.Label(root, text="Backup Tool", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# Source Directory
source_label = tk.Label(root, text="소스 디렉토리 선택", font=("Helvetica", 12))
source_label.grid(row=1, column=0, padx=10, pady=10)

source_entry = tk.Entry(root, width=40)
source_entry.grid(row=1, column=1, padx=10, pady=10)

source_button = tk.Button(root, text="파일선택", command=select_source_dir)
source_button.grid(row=1, column=2, padx=10, pady=10)

# Target Directory
target_label = tk.Label(root, text="목적지 디렉토리 선택", font=("Helvetica", 12))
target_label.grid(row=2, column=0, padx=10, pady=10)

target_entry = tk.Entry(root, width=40)
target_entry.grid(row=2, column=1, padx=10, pady=10)

target_button = tk.Button(root, text="파일선택", command=select_target_dir)
target_button.grid(row=2, column=2, padx=10, pady=10)

# Backup Buttons
backup_button = tk.Button(root, text="백업", command=backup)
backup_button.grid(row=3, column=0, padx=10, pady=20)

full_backup_button = tk.Button(root, text="풀백업", command=full_backup)
full_backup_button.grid(row=3, column=1, padx=10, pady=20)

incremental_backup_button = tk.Button(root, text="incremental 백업", command=incremental_backup)
incremental_backup_button.grid(row=3, column=2, padx=10, pady=20)

# Start the GUI event loop
root.mainloop()
