import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import os
import json
from PIL import Image, ImageTk

class CloudStorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("클라우드 스토리지")

        self.aws_access_key_id = ''
        self.aws_secret_access_key = ''
        self.bucket_name = ''

        self.load_credentials()
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(main_frame, text="클라우드 스토리지", font=("Helvetica", 16))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Bucket Frame
        bucket_frame = tk.LabelFrame(main_frame, text="버킷 작업", padx=10, pady=10)
        bucket_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.N)

        tk.Button(bucket_frame, text="버킷 생성", command=self.create_bucket, width=20).pack(pady=5)
        tk.Button(bucket_frame, text="버킷 선택", command=self.select_bucket, width=20).pack(pady=5)
        tk.Button(bucket_frame, text="버킷 삭제", command=self.delete_bucket, width=20).pack(pady=5)
        tk.Button(bucket_frame, text="자격 증명 재설정", command=self.reset_credentials, width=20).pack(pady=5)

        # File Frame
        file_frame = tk.LabelFrame(main_frame, text="파일 작업", padx=10, pady=10)
        file_frame.grid(row=1, column=1, padx=10, pady=10, sticky=tk.N)

        tk.Button(file_frame, text="파일 업로드", command=self.upload_file, width=20).pack(pady=5)
        tk.Button(file_frame, text="파일 다운로드", command=self.download_selected_file, width=20).pack(pady=5)
        tk.Button(file_frame, text="파일 삭제", command=self.delete_selected_file, width=20).pack(pady=5)
        tk.Button(file_frame, text="폴더 업로드", command=self.upload_folder, width=20).pack(pady=5)

        self.file_listbox = tk.Listbox(main_frame, selectmode=tk.SINGLE, width=50)
        self.file_listbox.grid(row=2, column=0, columnspan=2, pady=10)

        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=3, column=0, columnspan=2, pady=10)

        # Load back button image
        back_image = Image.open("캡처.PNG")  # 수정: 올바른 이미지 파일 경로로 변경
        back_image = back_image.resize((40, 40), Image.Resampling.LANCZOS)
        self.back_image = ImageTk.PhotoImage(back_image)
        
        self.back_button = tk.Button(main_frame, image=self.back_image, command=self.back_to_bucket_list, width=50, height=50)
        self.back_button.grid(row=4, column=1, padx=10, pady=10, sticky=tk.SE)
        self.back_button.grid_remove()

        self.update_bucket_list()

    def load_credentials(self):
        # 자격 증명을 파일에서 불러오기
        if os.path.exists("aws_credentials.json"):
            with open("aws_credentials.json", "r") as file:
                credentials = json.load(file)
                self.aws_access_key_id = credentials.get("aws_access_key_id", "")
                self.aws_secret_access_key = credentials.get("aws_secret_access_key", "")

    def save_credentials(self):
        # 자격 증명을 파일에 저장
        credentials = {
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key
        }
        with open("aws_credentials.json", "w") as file:
            json.dump(credentials, file)

    def reset_credentials(self):
        # 자격 증명 파일 삭제 및 새로운 자격 증명 입력
        if os.path.exists("aws_credentials.json"):
            os.remove("aws_credentials.json")
        self.aws_access_key_id = simpledialog.askstring("입력", "AWS 액세스 키 ID를 입력하세요")
        self.aws_secret_access_key = simpledialog.askstring("입력", "AWS 비밀 액세스 키를 입력하세요")
        self.save_credentials()
        messagebox.showinfo("성공", "자격 증명이 재설정되었습니다")

    def create_bucket(self):
        if not self.aws_access_key_id or not self.aws_secret_access_key:
            self.aws_access_key_id = simpledialog.askstring("입력", "AWS 액세스 키 ID를 입력하세요")
            self.aws_secret_access_key = simpledialog.askstring("입력", "AWS 비밀 액세스 키를 입력하세요")
            self.save_credentials()  # 자격 증명 저장

        s3 = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name='ap-northeast-2'
        )

        while True:
            self.bucket_name = simpledialog.askstring("입력", "새 버킷 이름을 입력하세요")
            try:
                s3.create_bucket(Bucket=self.bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})
                messagebox.showinfo("성공", "버킷이 성공적으로 생성되었습니다")
                break
            except ClientError as e:
                if e.response['Error']['Code'] == 'BucketAlreadyExists':
                    messagebox.showerror("오류", "버킷 이름이 이미 존재합니다. 다른 이름을 선택하세요.")
                elif e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                    messagebox.showinfo("정보", "버킷이 이미 존재합니다. 기존 버킷을 사용합니다.")
                    break
                else:
                    messagebox.showerror("오류", f"버킷 생성 실패: {e}")
                    return
        self.update_bucket_list()

    def select_bucket(self):
        selected_bucket = self.file_listbox.get(tk.ACTIVE)
        if not selected_bucket:
            messagebox.showerror("오류", "선택된 버킷이 없습니다")
            return

        self.bucket_name = selected_bucket
        self.title_label.config(text=f"버킷: {self.bucket_name} - 파일 목록")
        self.back_button.grid()
        self.update_file_list()

    def delete_bucket(self):
        selected_bucket = self.file_listbox.get(tk.ACTIVE)
        if not selected_bucket:
            messagebox.showerror("오류", "선택된 버킷이 없습니다")
            return

        s3 = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name='ap-northeast-2'
        )

        try:
            # 버킷 안의 모든 객체를 먼저 삭제
            response = s3.list_objects_v2(Bucket=selected_bucket)
            if 'Contents' in response:
                for item in response['Contents']:
                    s3.delete_object(Bucket=selected_bucket, Key=item['Key'])

            s3.delete_bucket(Bucket=selected_bucket)
            messagebox.showinfo("성공", "버킷이 성공적으로 삭제되었습니다")
            self.update_bucket_list()
        except ClientError as e:
            messagebox.showerror("오류", f"버킷 삭제 실패: {e}")

    def update_bucket_list(self):
        self.file_listbox.delete(0, tk.END)
        bucket_list = self.get_bucket_list()
        self.title_label.config(text="버킷 목록")
        for bucket in bucket_list:
            self.file_listbox.insert(tk.END, bucket)
        self.back_button.grid_remove()

    def back_to_bucket_list(self):
        self.bucket_name = ''
        self.update_bucket_list()

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        file_list = self.get_file_list()
        for file in file_list:
            self.file_listbox.insert(tk.END, file)

    def upload_file(self):
        if not self.bucket_name:
            messagebox.showerror("오류", "선택된 버킷이 없습니다")
            return

        file_path = filedialog.askopenfilename()
        if file_path:
            self.progress.start()
            try:
                s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, region_name='ap-northeast-2')
                s3.upload_file(file_path, self.bucket_name, file_path.split('/')[-1])
                messagebox.showinfo("성공", "파일이 성공적으로 업로드되었습니다")
                self.update_file_list()
            except FileNotFoundError:
                messagebox.showerror("오류", "파일을 찾을 수 없습니다")
            except NoCredentialsError:
                messagebox.showerror("오류", "자격 증명이 없습니다")
            finally:
                self.progress.stop()

    def download_selected_file(self):
        if not self.bucket_name:
            messagebox.showerror("오류", "선택된 버킷이 없습니다")
            return

        selected_file = self.file_listbox.get(tk.ACTIVE)
        if not selected_file:
            messagebox.showerror("오류", "선택된 파일이 없습니다")
            return
        self.download_file(selected_file)

    def delete_selected_file(self):
        if not self.bucket_name:
            messagebox.showerror("오류", "선택된 버킷이 없습니다")
            return

        selected_file = self.file_listbox.get(tk.ACTIVE)
        if not selected_file:
            messagebox.showerror("오류", "선택된 파일이 없습니다")
            return
        self.delete_file(selected_file)

    def download_file(self, file_name):
        save_path = filedialog.asksaveasfilename(initialfile=file_name)
        if save_path:
            self.progress.start()
            try:
                s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, region_name='ap-northeast-2')
                s3.download_file(self.bucket_name, file_name, save_path)
                messagebox.showinfo("성공", "파일이 성공적으로 다운로드되었습니다")
            except FileNotFoundError:
                messagebox.showerror("오류", "버킷에서 파일을 찾을 수 없습니다")
            except NoCredentialsError:
                messagebox.showerror("오류", "자격 증명이 없습니다")
            finally:
                self.progress.stop()

    def delete_file(self, file_name):
        if messagebox.askyesno("삭제", f"{file_name} 파일을 삭제하시겠습니까?"):
            self.progress.start()
            try:
                s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, region_name='ap-northeast-2')
                s3.delete_object(Bucket=self.bucket_name, Key=file_name)
                messagebox.showinfo("성공", "파일이 성공적으로 삭제되었습니다")
                self.update_file_list()
            except NoCredentialsError:
                messagebox.showerror("오류", "자격 증명이 없습니다")
            finally:
                self.progress.stop()

    def upload_folder(self):
        if not self.bucket_name:
            messagebox.showerror("오류", "선택된 버킷이 없습니다")
            return

        folder_path = filedialog.askdirectory()
        if folder_path:
            self.progress.start()
            try:
                s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, region_name='ap-northeast-2')
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        s3_path = os.path.relpath(file_path, folder_path)
                        s3.upload_file(file_path, self.bucket_name, s3_path)
                messagebox.showinfo("성공", "폴더가 성공적으로 업로드되었습니다")
                self.update_file_list()
            except FileNotFoundError:
                messagebox.showerror("오류", "폴더를 찾을 수 없습니다")
            except NoCredentialsError:
                messagebox.showerror("오류", "자격 증명이 없습니다")
            finally:
                self.progress.stop()

    def get_bucket_list(self):
        if not self.aws_access_key_id or not self.aws_secret_access_key:
            return []
        try:
            s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, region_name='ap-northeast-2')
            response = s3.list_buckets()
            return [bucket['Name'] for bucket in response['Buckets']]
        except NoCredentialsError:
            messagebox.showerror("오류", "자격 증명이 없습니다")
            return []

    def get_file_list(self):
        if not self.bucket_name:
            return []
        try:
            s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key, region_name='ap-northeast-2')
            response = s3.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                return [item['Key'] for item in response['Contents']]
            return []
        except NoCredentialsError:
            messagebox.showerror("오류", "자격 증명이 없습니다")
            return []

if __name__ == "__main__":
    root = tk.Tk()
    app = CloudStorageApp(root)
    root.mainloop()
