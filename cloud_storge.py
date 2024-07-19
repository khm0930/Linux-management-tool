import boto3
from botocore.exceptions import NoCredentialsError
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import os  # os 모듈 임포트

class CloudStorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cloud Storage")

        self.s3 = boto3.client('s3', region_name='ap-northeast-2')
        self.bucket_name = 'linuxtools3'  # 자신의 S3 버킷 이름으로 변경

        self.create_widgets()
        self.update_file_list()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Cloud Storage", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(frame, text="Upload File", command=self.upload_file).pack(pady=5)
        tk.Button(frame, text="Download File", command=self.download_selected_file).pack(pady=5)
        tk.Button(frame, text="Delete File", command=self.delete_selected_file).pack(pady=5)
        tk.Button(frame, text="Upload Folder", command=self.upload_folder).pack(pady=5)

        self.file_listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=50)
        self.file_listbox.pack(pady=10)

        self.progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        file_list = self.get_file_list()
        for file in file_list:
            self.file_listbox.insert(tk.END, file)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.progress.start()
            try:
                self.s3.upload_file(file_path, self.bucket_name, file_path.split('/')[-1])
                messagebox.showinfo("Success", "File uploaded successfully")
                self.update_file_list()
            except FileNotFoundError:
                messagebox.showerror("Error", "The file was not found")
            except NoCredentialsError:
                messagebox.showerror("Error", "Credentials not available")
            finally:
                self.progress.stop()

    def download_selected_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if not selected_file:
            messagebox.showerror("Error", "No file selected")
            return
        self.download_file(selected_file)

    def delete_selected_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if not selected_file:
            messagebox.showerror("Error", "No file selected")
            return
        self.delete_file(selected_file)

    def download_file(self, file_name):
        save_path = filedialog.asksaveasfilename(initialfile=file_name)
        if save_path:
            self.progress.start()
            try:
                self.s3.download_file(self.bucket_name, file_name, save_path)
                messagebox.showinfo("Success", "File downloaded successfully")
            except FileNotFoundError:
                messagebox.showerror("Error", "The file was not found in the bucket")
            except NoCredentialsError:
                messagebox.showerror("Error", "Credentials not available")
            finally:
                self.progress.stop()

    def delete_file(self, file_name):
        if messagebox.askyesno("Delete", f"Are you sure you want to delete {file_name}?"):
            self.progress.start()
            try:
                self.s3.delete_object(Bucket=self.bucket_name, Key=file_name)
                messagebox.showinfo("Success", "File deleted successfully")
                self.update_file_list()
            except NoCredentialsError:
                messagebox.showerror("Error", "Credentials not available")
            finally:
                self.progress.stop()

    def upload_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.progress.start()
            try:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        s3_path = os.path.relpath(file_path, folder_path)
                        self.s3.upload_file(file_path, self.bucket_name, s3_path)
                messagebox.showinfo("Success", "Folder uploaded successfully")
                self.update_file_list()
            except FileNotFoundError:
                messagebox.showerror("Error", "The folder was not found")
            except NoCredentialsError:
                messagebox.showerror("Error", "Credentials not available")
            finally:
                self.progress.stop()

    def get_file_list(self):
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                return [item['Key'] for item in response['Contents']]
            return []
        except NoCredentialsError:
            messagebox.showerror("Error", "Credentials not available")
            return []

if __name__ == "__main__":
    root = tk.Tk()
    app = CloudStorageApp(root)
    root.mainloop()
