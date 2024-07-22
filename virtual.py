import libvirt
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os
import subprocess
from PIL import Image, ImageTk

class VMManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("가상 머신 관리자")

        self.conn = libvirt.open('qemu:///system')

        self.create_widgets()
        self.update_vm_list()

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.vm_listbox = tk.Listbox(main_frame, selectmode=tk.SINGLE, width=50)
        self.vm_listbox.pack(pady=10)

        tk.Button(main_frame, text="가상 머신 생성", command=self.create_vm).pack(pady=5)
        tk.Button(main_frame, text="가상 머신 시작", command=self.start_vm).pack(pady=5)
        tk.Button(main_frame, text="가상 머신 중지", command=self.stop_vm).pack(pady=5)
        tk.Button(main_frame, text="가상 머신 재시작", command=self.restart_vm).pack(pady=5)
        tk.Button(main_frame, text="가상 머신 삭제", command=self.delete_vm).pack(pady=5)

    def update_vm_list(self):
        self.vm_listbox.delete(0, tk.END)
        for id in self.conn.listDomainsID():
            dom = self.conn.lookupByID(id)
            self.vm_listbox.insert(tk.END, dom.name())
        for name in self.conn.listDefinedDomains():
            self.vm_listbox.insert(tk.END, name)

    def ask_sudo_password(self):
        return simpledialog.askstring("sudo 비밀번호 입력", "sudo 비밀번호를 입력하세요", show='*')

    def create_vm(self):
        vm_name = simpledialog.askstring("입력", "가상 머신 이름을 입력하세요")
        if vm_name:
            disk_path = f"/var/lib/libvirt/images/{vm_name}.qcow2"
            iso_path = filedialog.askopenfilename(title="ISO 파일 선택", filetypes=[("ISO files", "*.iso")])
            if not iso_path:
                return

            sudo_password = self.ask_sudo_password()
            if not sudo_password:
                messagebox.showerror("오류", "sudo 비밀번호가 필요합니다.")
                return

            self.create_disk_image(disk_path, sudo_password)

            xml = f"""
            <domain type='kvm'>
                <name>{vm_name}</name>
                <memory unit='KiB'>1048576</memory>
                <vcpu placement='static'>1</vcpu>
                <os>
                    <type arch='x86_64' machine='pc-i440fx-2.9'>hvm</type>
                    <boot dev='cdrom'/>
                    <boot dev='hd'/>
                </os>
                <devices>
                    <disk type='file' device='disk'>
                        <driver name='qemu' type='qcow2'/>
                        <source file='{disk_path}'/>
                        <target dev='vda' bus='virtio'/>
                        <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
                    </disk>
                    <disk type='file' device='cdrom'>
                        <driver name='qemu' type='raw'/>
                        <source file='{iso_path}'/>
                        <target dev='sda' bus='sata'/>
                        <readonly/>
                    </disk>
                    <interface type='network'>
                        <mac address='52:54:00:6b:29:23'/>
                        <source network='default'/>
                        <model type='virtio'/>
                        <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
                    </interface>
                    <graphics type='vnc' port='-1' autoport='yes'/>
                </devices>
            </domain>
            """
            try:
                self.conn.createXML(xml, 0)
                messagebox.showinfo("성공", "가상 머신이 성공적으로 생성되었습니다")
                self.update_vm_list()
                self.start_vm_directly(vm_name)
            except libvirt.libvirtError as e:
                messagebox.showerror("오류", f"가상 머신 생성 실패: {e}")

    def create_disk_image(self, disk_path, sudo_password):
        try:
            subprocess.run(['sudo', '-S', 'qemu-img', 'create', '-f', 'qcow2', disk_path, '10G'], input=sudo_password.encode(), check=True)
            subprocess.run(['sudo', '-S', 'chown', 'libvirt-qemu:kvm', disk_path], input=sudo_password.encode(), check=True)
            subprocess.run(['sudo', '-S', 'chmod', '666', disk_path], input=sudo_password.encode(), check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("오류", f"디스크 이미지 생성 실패: {e}")

    def start_vm(self):
        selected_vm = self.vm_listbox.get(tk.ACTIVE)
        if not selected_vm:
            messagebox.showerror("오류", "선택된 가상 머신이 없습니다")
            return

        dom = self.conn.lookupByName(selected_vm)
        if dom.isActive() == 1:
            messagebox.showinfo("정보", "가상 머신이 이미 실행 중입니다")
            return

        try:
            dom.create()
            subprocess.run(['sudo', 'virt-viewer', selected_vm])
            messagebox.showinfo("성공", "가상 머신이 성공적으로 시작되었습니다")
        except libvirt.libvirtError as e:
            messagebox.showerror("오류", f"가상 머신 시작 실패: {e}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("오류", f"virt-viewer 실행 실패: {e}")

    def stop_vm(self):
        selected_vm = self.vm_listbox.get(tk.ACTIVE)
        if not selected_vm:
            messagebox.showerror("오류", "선택된 가상 머신이 없습니다")
            return

        dom = self.conn.lookupByName(selected_vm)
        if dom.isActive() != 1:
            messagebox.showinfo("정보", "가상 머신이 이미 중지되어 있습니다")
            return

        try:
            dom.shutdown()
            messagebox.showinfo("성공", "가상 머신이 성공적으로 중지되었습니다")
        except libvirt.libvirtError as e:
            messagebox.showerror("오류", f"가상 머신 중지 실패: {e}")

    def restart_vm(self):
        selected_vm = self.vm_listbox.get(tk.ACTIVE)
        if not selected_vm:
            messagebox.showerror("오류", "선택된 가상 머신이 없습니다")
            return

        dom = self.conn.lookupByName(selected_vm)
        try:
            dom.reboot()
            messagebox.showinfo("성공", "가상 머신이 성공적으로 재시작되었습니다")
        except libvirt.libvirtError as e:
            messagebox.showerror("오류", f"가상 머신 재시작 실패: {e}")

    def delete_vm(self):
        selected_vm = self.vm_listbox.get(tk.ACTIVE)
        if not selected_vm:
            messagebox.showerror("오류", "선택된 가상 머신이 없습니다")
            return

        try:
            dom = self.conn.lookupByName(selected_vm)
            if dom.isActive() == 1:
                dom.destroy()
            dom.undefine()
            messagebox.showinfo("성공", "가상 머신이 성공적으로 삭제되었습니다")
            self.update_vm_list()
        except libvirt.libvirtError as e:
            messagebox.showerror("오류", f"가상 머신 삭제 실패: {e}")
        except libvirt.libvirtError:
            messagebox.showerror("오류", f"가상 머신을 찾을 수 없습니다: {selected_vm}")

    def start_vm_directly(self, vm_name):
        try:
            subprocess.run(['sudo', 'virt-viewer', vm_name], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("오류", f"가상 머신 시작 실패: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VMManagerApp(root)
    root.mainloop()
