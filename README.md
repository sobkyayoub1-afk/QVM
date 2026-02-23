# QVM
Description:
QVM is a lightweight Python-based GUI for managing and interacting with QEMU virtual machines on macOS. It provides an intuitive interface for launching, controlling, and monitoring virtual machines without using the command line. Designed to be easy to use for beginners while still powerful for advanced users, QVM streamlines your virtual machine workflow.

Features:

Launch and manage QEMU virtual machines directly from the GUI

Simple, clean, and responsive Python interface

Fully open-source and customizable

Pre-built macOS releases available for quick setup

Installation:

Download the latest macOS release from the Releases tab

Open the app and start managing your virtual machines immediately

License:
MIT License – free and open source for personal and commercial use





⚠️ Permissions Note

QVM needs to run with administrator privileges (sudo) to create and manage QEMU virtual machine files.



(adjust path if you placed the app elsewhere)

Running without sudo may result in permission errors when creating VMs or saving VM configurations.

macOS may ask for your password when running with sudo. This is normal.

Do not run as root unnecessarily—only use sudo for starting the app.

All VM files will be created under your user directory (or the paths you configure), but elevated privileges are required for proper file creation.





Redirecting the VMs Folder to the Project Root (note)

By default, QVM creates the VMs folder inside the app bundle (qemugui.app/Contents/Resources/VMs). To make it easier to find and manage your virtual machines, you can redirect this folder to the VMs folder in the root of the project you downloaded.

Steps:

Open Terminal.

Navigate to the Resources folder inside the app bundle:

cd /path/to/QVM/qemugui.app/Contents/Resources

Create a symbolic link pointing to the project root VMs folder:

ln -s /path/to/QVM/VMs VMs

Replace /path/to/QVM with the full path to your project folder.

After this, whenever QVM tries to create or access a VM in Resources/VMs, it will automatically read/write from the VMs folder in your project root.
