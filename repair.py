import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import hashlib
import threading
import logging
import os

# Configure logging
logging.basicConfig(filename="windows_repair.log", level=logging.INFO,
                    format="%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

def calculate_hash(file_path):
    # Calculate the SHA-256 hash of a file
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def check_and_repair_windows():
    try:
        # Step 1: Check and repair Windows files using DISM tool
        subprocess.run(["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"], check=True)

        # Step 2: Check system files using System File Checker (SFC)
        subprocess.run(["sfc", "/scannow"], check=True)

        messagebox.showinfo("Success", "Windows files checked and repaired successfully!")
        logging.info("Windows files checked and repaired successfully")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")

def run_memory_test():
    # Placeholder for memory test functionality
    messagebox.showinfo("Memory Test", "Memory test not implemented yet.")
    logging.info("Memory test not implemented")

def disk_cleanup():
    try:
        # Run the Disk Cleanup utility
        subprocess.run(["cleanmgr", "/sagerun:1"], check=True)
        messagebox.showinfo("Success", "Disk cleanup completed successfully!")
        logging.info("Disk cleanup completed successfully")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred during disk cleanup: {e}")
        logging.error(f"An error occurred during disk cleanup: {e}")

def check_disk_errors():
    try:
        # Run the Check Disk utility to check for disk errors
        subprocess.run(["chkdsk", "/f"], check=True)
        messagebox.showinfo("Success", "Disk error check completed successfully!")
        logging.info("Disk error check completed successfully")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred during disk error check: {e}")
        logging.error(f"An error occurred during disk error check: {e}")

def update_system():
    try:
        # Run the Windows Update task to initiate system update
        subprocess.run(["schtasks", "/run", "/tn", "Microsoft\\Windows\\WindowsUpdate\\Automatic App Update"], check=True)
        messagebox.showinfo("Success", "System update initiated successfully!")
        logging.info("System update initiated successfully")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred during system update: {e}")
        logging.error(f"An error occurred during system update: {e}")

def perform_action(action_func, action_name):
    # Perform an action in a separate thread to avoid freezing the GUI
    action_thread = threading.Thread(target=action_func, daemon=True)
    action_thread.start()
    messagebox.showinfo("Action Started", f"{action_name} in progress. Check logs for details.")

# Create GUI
class WindowsRepairApp:
    def __init__(self, master):
        self.master = master
        master.title("Windows Repair Utility")
        master.geometry("600x400")

        style = ttk.Style()
        style.theme_use("clam")

        self.create_widgets()

    def create_widgets(self):
        # Create buttons for different repair options
        self.button_check_repair = ttk.Button(self.master, text="Check & Repair Windows Installation",
                                              command=lambda: perform_action(self.check_and_repair_windows, "Check & Repair"),
                                              style="Action.TButton")
        self.button_check_repair.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        self.button_memory_test = ttk.Button(self.master, text="Run Memory Test on Startup",
                                             command=lambda: perform_action(self.run_memory_test, "Run Memory Test"),
                                             style="Action.TButton")
        self.button_memory_test.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        self.button_disk_cleanup = ttk.Button(self.master, text="Disk Cleanup",
                                              command=lambda: perform_action(self.disk_cleanup, "Disk Cleanup"),
                                              style="Action.TButton")
        self.button_disk_cleanup.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        self.button_check_disk_errors = ttk.Button(self.master, text="Check Disk Errors",
                                                   command=lambda: perform_action(self.check_disk_errors, "Check Disk Errors"),
                                                   style="Action.TButton")
        self.button_check_disk_errors.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        self.button_update_system = ttk.Button(self.master, text="Update System",
                                               command=lambda: perform_action(self.update_system, "Update System"),
                                               style="Action.TButton")
        self.button_update_system.grid(row=4, column=0, pady=10, padx=10, sticky="ew")

        self.button_close = ttk.Button(self.master, text="Close", command=self.master.destroy, style="Close.TButton")
        self.button_close.grid(row=5, column=0, pady=10, padx=10, sticky="ew")

        # Tooltips
        self.button_check_repair.tooltip = ttk.ToolTip(self.master, "Check and repair Windows installation")
        self.button_memory_test.tooltip = ttk.ToolTip(self.master, "Run memory test on startup")
        self.button_disk_cleanup.tooltip = ttk.ToolTip(self.master, "Perform disk cleanup")
        self.button_check_disk_errors.tooltip = ttk.ToolTip(self.master, "Check for disk errors")
        self.button_update_system.tooltip = ttk.ToolTip(self.master, "Initiate system update")
        self.button_close.tooltip = ttk.ToolTip(self.master, "Close the program")

def main():
    # Configure styles
    root = tk.Tk()
    style = ttk.Style(root)
    style.configure("Action.TButton", foreground="green", font=("Arial", 12, "bold"))
    style.configure("Close.TButton", foreground="red", font=("Arial", 12, "bold"))

    app = WindowsRepairApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
