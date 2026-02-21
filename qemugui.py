#!/usr/bin/env python3
import os
import subprocess
import json
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

# Base directory for VMs
BASE_DIR = os.path.join(os.getcwd(), "VMs")
os.makedirs(BASE_DIR, exist_ok=True)

# QEMU binary path
QEMU_BIN = "/opt/homebrew/bin/qemu-system-x86_64"
QEMU_IMG = "/opt/homebrew/bin/qemu-img"

# Load existing VM config
def load_vm_config(vm_name):
    cfg_path = os.path.join(BASE_DIR, vm_name, "config.json")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r") as f:
            return json.load(f)
    return None

# Save VM config
def save_vm_config(vm_name, config):
    vm_path = os.path.join(BASE_DIR, vm_name)
    os.makedirs(vm_path, exist_ok=True)
    cfg_path = os.path.join(vm_path, "config.json")
    with open(cfg_path, "w") as f:
        json.dump(config, f, indent=2)

# Create a new VM
def create_vm():
    vm_name = simpledialog.askstring("VM Name", "Enter VM name:")
    if not vm_name:
        return

    vm_path = os.path.join(BASE_DIR, vm_name)
    os.makedirs(vm_path, exist_ok=True)
    disk_path = os.path.join(vm_path, "disk.qcow2")

    # User options
    ram_mb = simpledialog.askinteger("RAM", "Enter RAM in MB:", minvalue=512, maxvalue=65536)
    cpu_cores = simpledialog.askinteger("CPU", "Enter number of CPU cores:", minvalue=1, maxvalue=32)
    disk_mb = simpledialog.askinteger("Disk", "Enter disk size in MB:", minvalue=512, maxvalue=1048576)  # 1 TB max
    iso_path = filedialog.askopenfilename(title="Select Boot ISO", filetypes=[("ISO Files", "*.iso")])
    machine_type = simpledialog.askstring("Machine Type", "Enter machine type (e.g., q35, pc):", initialvalue="q35")
    accel = simpledialog.askstring("Acceleration", "Enter accelerator (tcg recommended on mac):", initialvalue="tcg")

    # Create QCOW2 disk
    if not os.path.exists(disk_path):
        subprocess.run([
            QEMU_IMG, "create", "-f", "qcow2", disk_path, f"{disk_mb}M"
        ], check=True)

    # Save config
    config = {
        "ram_mb": ram_mb,
        "cpu_cores": cpu_cores,
        "disk_path": disk_path,
        "iso_path": iso_path,
        "machine_type": machine_type,
        "accel": accel
    }
    save_vm_config(vm_name, config)
    messagebox.showinfo("VM Created", f"VM '{vm_name}' configuration saved!")

# Start a VM
def start_vm():
    vm_name = simpledialog.askstring("VM Name", "Enter VM name to start:")
    config = load_vm_config(vm_name)
    if not config:
        messagebox.showerror("Error", f"No config found for VM '{vm_name}'")
        return

    disk_path = config["disk_path"]
    iso_path = config.get("iso_path")
    ram_mb = config["ram_mb"]
    cpu_cores = config["cpu_cores"]
    machine_type = config.get("machine_type", "q35")
    accel = config.get("accel", "tcg")

    qemu_cmd = [
        QEMU_BIN,
        "-m", str(ram_mb),
        "-smp", str(cpu_cores),
        "-machine", machine_type,
        "-accel", accel,
        "-drive", f"file={disk_path},format=qcow2,if=virtio,cache=writeback"
    ]

    if iso_path and os.path.exists(iso_path):
        qemu_cmd += ["-cdrom", iso_path, "-boot", "d"]
    else:
        qemu_cmd += ["-boot", "c"]

    subprocess.run(qemu_cmd)

# Tkinter UI
root = tk.Tk()
root.title("QEMU GUI Manager")

tk.Button(root, text="Create New VM", width=30, command=create_vm).pack(pady=10)
tk.Button(root, text="Start Existing VM", width=30, command=start_vm).pack(pady=10)
tk.Button(root, text="Exit", width=30, command=root.destroy).pack(pady=10)

root.mainloop()
