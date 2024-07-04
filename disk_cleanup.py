import tkinter as tk
from tkinter import messagebox, filedialog
import os
import shutil
import time
import hashlib
import threading
import psutil
import matplotlib.pyplot as plt

TRASH_FOLDER = os.path.expanduser("~/.local/share/Trash/files")

# 휴지통 폴더 생성
if not os.path.exists(TRASH_FOLDER):
    os.makedirs(TRASH_FOLDER)

# 오래된 파일을 휴지통으로 이동하는 함수
def move_old_files_to_trash(folder_path, days_old):
    now = time.time()
    cutoff = now - (days_old * 86400)
    
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.getmtime(file_path) < cutoff:
                shutil.move(file_path, TRASH_FOLDER)
                print(f"Moved {file_path} to trash")

# 파일 복구 함수
def restore_files_from_trash():
    for root, dirs, files in os.walk(TRASH_FOLDER):
        for filename in files:
            trash_file_path = os.path.join(root, filename)
            original_file_path = os.path.join(folder_path, filename)  # 원래 파일 경로 지정 필요
            shutil.move(trash_file_path, original_file_path)
            print(f"Restored {trash_file_path} to {original_file_path}")

# 휴지통 비우기 함수
def empty_trash():
    for root, dirs, files in os.walk(TRASH_FOLDER):
        for filename in files:
            file_path = os.path.join(root, filename)
            os.remove(file_path)
            print(f"Deleted {file_path} from trash")

# 중복 파일 찾기 및 삭제 함수
def find_and_delete_duplicates(folder_path):
    hashes = {}
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_hash = hash_file(file_path)
            if file_hash in hashes:
                shutil.move(file_path, TRASH_FOLDER)
                print(f"Moved duplicate file {file_path} to trash")
            else:
                hashes[file_hash] = file_path

def hash_file(file_path):
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

# 임시 파일 및 캐시 삭제 함수
def delete_temp_and_cache_files():
    temp_folders = ["/tmp", "/var/tmp"]
    cache_folders = [os.path.expanduser("~/.cache")]

    for folder in temp_folders + cache_folders:
        for root, dirs, files in os.walk(folder):
            for file in files:
                try:
                    shutil.move(os.path.join(root, file), TRASH_FOLDER)
                    print(f"Moved {os.path.join(root, file)} to trash")
                except Exception as e:
                    print(f"Failed to move {os.path.join(root, file)} to trash: {e}")

# 시스템 성능 모니터링 함수
def monitor_system_performance():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    info = f"CPU 사용률: {cpu_usage}%\n메모리 사용률: {memory_usage}%\n디스크 사용률: {disk_usage}%"
    print(info)
    messagebox.showinfo("시스템 성능", info)

# 자동 정리 일정 설정 함수
def schedule_cleanup():
    while True:
        perform_disk_cleanup()
        time.sleep(86400)  # 24시간마다 정리 수행

# 보안 삭제 함수
def secure_delete(file_path):
    with open(file_path, "ba+", buffering=0) as delfile:
        length = delfile.tell()
        for _ in range(3):
            delfile.seek(0)
            delfile.write(os.urandom(length))
    os.remove(file_path)
    print(f"Securely deleted {file_path}")

# GUI에서 디스크 정리 작업을 수행하는 함수
def perform_disk_cleanup():
    folder_path = filedialog.askdirectory()
    if not folder_path:
        messagebox.showwarning("경고", "폴더를 선택해주세요.")
        return

    move_old_files_to_trash(folder_path, 30)
    move_files_by_extension(folder_path, os.path.join(folder_path, "Images"), ".jpg")
    move_files_by_extension(folder_path, os.path.join(folder_path, "Images"), ".png")
    move_files_by_extension(folder_path, os.path.join(folder_path, "Documents"), ".pdf")
    move_files_by_extension(folder_path, os.path.join(folder_path, "Documents"), ".docx")
    find_and_delete_duplicates(folder_path)
    delete_temp_and_cache_files()

    messagebox.showinfo("성공", "디스크 정리가 완료되었습니다.")

# 디스크 분석 및 시각화 함수
def analyze_and_visualize_disk_usage():
    folder_path = filedialog.askdirectory()
    if not folder_path:
        messagebox.showwarning("경고", "폴더를 선택해주세요.")
        return

    total_size = 0
    folder_sizes = {}

    for root, dirs, files in os.walk(folder_path):
        folder_size = 0
        for file in files:
            file_path = os.path.join(root, file)
            folder_size += os.path.getsize(file_path)
        folder_sizes[root] = folder_size
        total_size += folder_size

    folders = list(folder_sizes.keys())
    sizes = list(folder_sizes.values())

    # 폴더 이름만 레이블로 표시하고, 전체 경로는 콘솔에 출력
    folder_labels = [os.path.basename(folder) for folder in folders]
    for folder, size in folder_sizes.items():
        print(f"{folder}: {size} bytes")

    plt.figure(figsize=(10, 6))
    wedges, texts, autotexts = plt.pie(sizes, labels=None, autopct='%1.1f%%', textprops=dict(color="w"))

    # 차트 외부에 숫자만 표시하고 레이블은 차트 내부에 표시
    for i, text in enumerate(texts):
        text.set_text("")
        if sizes[i] > 0:
            plt.text(wedges[i].theta2 - (wedges[i].theta2 - wedges[i].theta1) / 2, wedges[i].r / 2,
                     folder_labels[i], ha='center', va='center', rotation=text.get_rotation())

    # 레전드 추가
    plt.legend(wedges, folder_labels, title="폴더 경로", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.title("디스크 사용량 분석")
    plt.show()

# 메인 윈도우 생성
root = tk.Tk()
root.title("디스크 정리 도구")
root.geometry("400x500")

# 설명 레이블
label = tk.Label(root, text="디스크 정리 도구", font=("Helvetica", 16))
label.pack(pady=10)

# 정리 버튼
cleanup_button = tk.Button(root, text="디스크 정리", command=perform_disk_cleanup, width=20)
cleanup_button.pack(pady=5)

# 중복 파일 삭제 버튼
duplicate_button = tk.Button(root, text="중복 파일 삭제", command=lambda: find_and_delete_duplicates(filedialog.askdirectory()), width=20)
duplicate_button.pack(pady=5)

# 임시 파일 및 캐시 삭제 버튼
temp_cache_button = tk.Button(root, text="임시 파일 및 캐시 삭제", command=delete_temp_and_cache_files, width=20)
temp_cache_button.pack(pady=5)

# 시스템 성능 모니터링 버튼
monitor_button = tk.Button(root, text="시스템 성능 모니터링", command=monitor_system_performance, width=20)
monitor_button.pack(pady=5)

# 디스크 분석 및 시각화 버튼
analyze_button = tk.Button(root, text="디스크 분석 및 시각화", command=analyze_and_visualize_disk_usage, width=20)
analyze_button.pack(pady=5)

# 보안 삭제 버튼
secure_delete_button = tk.Button(root, text="보안 삭제", command=lambda: secure_delete(filedialog.askopenfilename()), width=20)
secure_delete_button.pack(pady=5)

# 자동 정리 일정 설정 버튼
schedule_button = tk.Button(root, text="자동 정리 일정 설정", command=lambda: threading.Thread(target=schedule_cleanup).start(), width=20)
schedule_button.pack(pady=5)

# 파일 복구 버튼
restore_button = tk.Button(root, text="파일 복구", command=restore_files_from_trash, width=20)
restore_button.pack(pady=5)

# 휴지통 비우기 버튼
empty_trash_button = tk.Button(root, text="휴지통 비우기", command=empty_trash, width=20)
empty_trash_button.pack(pady=5)

# 메인 루프 실행
root.mainloop()
