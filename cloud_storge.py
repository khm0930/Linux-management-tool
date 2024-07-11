import boto3
from tkinter import messagebox

class CloudStorage:
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_file(self, file_name):
        try:
            self.s3.upload_file(file_name, self.bucket_name, file_name)
            messagebox.showinfo("Cloud Storage", "파일 업로드 성공")
        except Exception as e:
            messagebox.showerror("Cloud Storage", f"파일 업로드 실패: {e}")

if __name__ == "__main__":
    bucket_name = 'your-bucket-name'
    file_name = 'path/to/your/file'
    storage = CloudStorage(bucket_name)
    storage.upload_file(file_name)
