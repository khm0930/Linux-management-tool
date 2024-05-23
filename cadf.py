import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Compressor")
        self.geometry("450x250")
        
        # 'Compress File' 버튼
        self.compress_button = tk.Button(self, text="Compress File", command=self.compress_file)
        self.compress_button.pack(pady=10)
        
        # 'Compress Directory' 버튼
        self.compress_dir_button = tk.Button(self, text="Compress Directory", command=self.compress_directory)
        self.compress_dir_button.pack(pady=10)
        
        # 'Decompress File' 버튼
        self.decompress_button = tk.Button(self, text="Decompress File", command=self.decompress_file)
        self.decompress_button.pack(pady=10)
        
        # 'Decompress Directory' 버튼
        self.decompress_dir_button = tk.Button(self, text="Decompress Directory", command=self.decompress_directory)
        self.decompress_dir_button.pack(pady=10)
        
    def compress_file(self):
        file_path = filedialog.askopenfilename(title="Select a File to Compress", filetypes=(("All files", "*.*"),))
        if file_path:
            output_path = filedialog.asksaveasfilename(title="Save Compressed File As", defaultextension=".zip")
            if output_path:
                try:
                    with zipfile.ZipFile(output_path, 'w') as zipf:
                        zipf.write(file_path, os.path.basename(file_path))
                    messagebox.showinfo("Success", "File compressed successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error compressing file: {e}")

    def compress_directory(self):
        directory_path = filedialog.askdirectory(title="Select a Directory to Compress")
        if directory_path:
            output_path = filedialog.asksaveasfilename(title="Save Compressed Directory As", defaultextension=".zip")
            if output_path:
                try:
                    with zipfile.ZipFile(output_path, 'w') as zipf:
                        for root, dirs, files in os.walk(directory_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                zipf.write(file_path, os.path.relpath(file_path, directory_path))
                    messagebox.showinfo("Success", "Directory compressed successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error compressing directory: {e}")

    def decompress_file(self):
        file_path = filedialog.askopenfilename(title="Select a File to Decompress", filetypes=(("Zip files", "*.zip"),))
        if file_path:
            output_path = filedialog.askdirectory(title="Select Directory to Decompress")
            if output_path:
                try:
                    with zipfile.ZipFile(file_path, 'r') as zipf:
                        zipf.extractall(output_path)
                    messagebox.showinfo("Success", "File decompressed successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error decompressing file: {e}")
                    
    def decompress_directory(self):
        file_path = filedialog.askopenfilename(title="Select a Directory to Decompress", filetypes=(("Zip files", "*.zip"),))
        if file_path:
            output_path = filedialog.askdirectory(title="Select Directory to Decompress")
            if output_path:
                try:
                    with zipfile.ZipFile(file_path, 'r') as zipf:
                        zipf.extractall(output_path)
                    messagebox.showinfo("Success", "Directory decompressed successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error decompressing directory: {e}")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
