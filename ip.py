import tkinter as tk
from tkinter import messagebox
from subprocess import run

def set_static_ip():
    ip_address = ip_entry.get()
    subnet_mask = subnet_entry.get()
    gateway = gateway_entry.get()
    dns_servers = dns_entry.get()

    interface_name = 'enp6s0'  # 인터페이스 이름은 해당 시스템에 따라 다를 수 있습니다.

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

# GUI 생성
root = tk.Tk()
root.title('IP Configuration')

# 레이블 및 입력 필드 추가
tk.Label(root, text="IP Address:").grid(row=0)
tk.Label(root, text="Subnet Mask:").grid(row=1)
tk.Label(root, text="Gateway:").grid(row=2)
tk.Label(root, text="DNS Servers:").grid(row=3)

ip_entry = tk.Entry(root)
subnet_entry = tk.Entry(root)
gateway_entry = tk.Entry(root)
dns_entry = tk.Entry(root)

ip_entry.grid(row=0, column=1)
subnet_entry.grid(row=1, column=1)
gateway_entry.grid(row=2, column=1)
dns_entry.grid(row=3, column=1)

# 설정 버튼 추가
tk.Button(root, text='Set IP', command=set_static_ip).grid(row=4, column=0, columnspan=2)

root.mainloop()
