import tkinter as tk
from tkinter import ttk, messagebox
from subprocess import run
import psutil

def get_default_interface():
    # 현재 활성화된 네트워크 인터페이스 이름 가져오기
    addrs = psutil.net_if_addrs()
    for interface in addrs:
        if interface != 'lo':  # 'lo'는 루프백 인터페이스로 제외
            return interface
    return None

def set_static_ip():
    ip_address = ip_entry.get()
    subnet_mask = subnet_entry.get()
    gateway = gateway_entry.get()
    dns_servers = dns_entry.get()

    interface_name = get_default_interface()  # 시스템의 기본 네트워크 인터페이스 이름 가져오기

    # 새로운 설정
    static_ip_config = f"""
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    {interface_name}:
      addresses: [{ip_address}/{subnet_mask}]
      gateway4: {gateway}
      nameservers:
          addresses: [{dns_servers}]
"""

    # netplan 설정 파일의 경로
    config_path = '/etc/netplan/01-network-manager-all.yaml'

    try:
        # 변경된 설정 파일 쓰기
        with open(config_path, 'w') as file:
            file.write(static_ip_config)

        # 변경된 설정 적용
        run(['sudo', 'netplan', 'apply'])

        messagebox.showinfo('Success', 'IP settings applied successfully.')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {str(e)}')

def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(foreground='grey')

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(foreground='black')

    def on_focus_out(event):
        if entry.get() == '':
            entry.insert(0, placeholder_text)
            entry.config(foreground='grey')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# GUI 생성
root = tk.Tk()
root.title('IP Configuration')
root.geometry('400x300')

style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12), padding=10)

# 프레임 생성
frame = ttk.Frame(root, padding="10 10 10 10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 레이블 및 입력 필드 추가
ttk.Label(frame, text="IP Address:").grid(row=0, column=0, sticky=tk.W, pady=5)
ttk.Label(frame, text="Subnet Mask:").grid(row=1, column=0, sticky=tk.W, pady=5)
ttk.Label(frame, text="Gateway:").grid(row=2, column=0, sticky=tk.W, pady=5)
ttk.Label(frame, text="DNS Servers:").grid(row=3, column=0, sticky=tk.W, pady=5)

ip_entry = ttk.Entry(frame, width=25)
subnet_entry = ttk.Entry(frame, width=25)
gateway_entry = ttk.Entry(frame, width=25)
dns_entry = ttk.Entry(frame, width=25)

ip_entry.grid(row=0, column=1, pady=5)
subnet_entry.grid(row=1, column=1, pady=5)
gateway_entry.grid(row=2, column=1, pady=5)
dns_entry.grid(row=3, column=1, pady=5)

# 예시 텍스트 추가
add_placeholder(ip_entry, '192.168.1.100')
add_placeholder(subnet_entry, '24')
add_placeholder(gateway_entry, '192.168.1.1')
add_placeholder(dns_entry, '8.8.8.8, 8.8.4.4')

# 설정 버튼 추가
ttk.Button(frame, text='Set IP', command=set_static_ip).grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()
