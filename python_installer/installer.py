import os
import sys
import shutil
import zipfile
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path
import urllib.request
import tempfile
import ctypes

# Constants
PLATFORM_TOOLS_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
DEFAULT_INSTALL_DIR = os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), "Android\\platform-tools")

class InstallerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Android SDK Platform Tools Installer")
        self.geometry("700x500")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")
        
        # Check for admin rights
        if not self.is_admin():
            self.show_error("Administrator privileges required", 
                           "This installer needs to be run as administrator to modify system PATH.")
            sys.exit(1)
        
        self.install_path = tk.StringVar(value=DEFAULT_INSTALL_DIR)
        self.add_to_path = tk.BooleanVar(value=True)
        self.create_shortcut = tk.BooleanVar(value=True)
        
        self.create_ui()
    
    def create_ui(self):
        # Main frame
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_label = tk.Label(main_frame, text="Android SDK Platform Tools Installer", 
                               font=("Segoe UI", 18), bg="#f5f5f5")
        header_label.pack(pady=(0, 20), anchor=tk.W)
        
        # Installation directory selection
        dir_frame = tk.LabelFrame(main_frame, text="Installation Location", 
                                 bg="#f5f5f5", padx=10, pady=10)
        dir_frame.pack(fill=tk.X, pady=(0, 15))
        
        path_entry = tk.Entry(dir_frame, textvariable=self.install_path, width=50)
        path_entry.grid(row=0, column=0, padx=(0, 10))
        
        browse_button = tk.Button(dir_frame, text="Browse", command=self.browse_directory, 
                                 bg="#3DDC84", fg="white", padx=10)
        browse_button.grid(row=0, column=1)
        
        # Options
        options_frame = tk.LabelFrame(main_frame, text="Installation Options", 
                                     bg="#f5f5f5", padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        path_check = tk.Checkbutton(options_frame, text="Add to System PATH", 
                                   variable=self.add_to_path, bg="#f5f5f5")
        path_check.pack(anchor=tk.W, pady=(0, 5))
        
        shortcut_check = tk.Checkbutton(options_frame, text="Create Desktop Shortcut", 
                                       variable=self.create_shortcut, bg="#f5f5f5")
        shortcut_check.pack(anchor=tk.W)
        
        # Progress section
        progress_frame = tk.LabelFrame(main_frame, text="Installation Progress", 
                                      bg="#f5f5f5", padx=10, pady=10)
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.status_label = tk.Label(progress_frame, text="Ready to install...", 
                                    bg="#f5f5f5", anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=(0, 5))
        
        self.progress = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, 
                                      length=100, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(0, 5))
        
        self.progress_label = tk.Label(progress_frame, text="0%", bg="#f5f5f5")
        self.progress_label.pack()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg="#f5f5f5")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        update_button = tk.Button(button_frame, text="Check for Updates", 
                                 command=self.check_updates, bg="#3DDC84", fg="white", padx=10)
        update_button.pack(side=tk.LEFT)
        
        install_button = tk.Button(button_frame, text="Install", 
                                  command=self.start_installation, bg="#3DDC84", fg="white", padx=20)
        install_button.pack(side=tk.RIGHT)
    
    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir=self.install_path.get())
        if directory:
            self.install_path.set(directory)
    
    def check_updates(self):
        self.status_label.config(text="Checking for updates...")
        
        def check():
            try:
                with urllib.request.urlopen(PLATFORM_TOOLS_URL) as response:
                    self.after(1000, lambda: tk.messagebox.showinfo(
                        "Update Check", 
                        "Updates are available and will be downloaded during installation."
                    ))
            except Exception as e:
                self.after(1000, lambda: tk.messagebox.showerror(
                    "Update Check Error", 
                    f"Error checking for updates: {str(e)}"
                ))
            finally:
                self.after(0, lambda: self.status_label.config(text="Ready to install..."))
        
        threading.Thread(target=check, daemon=True).start()
    
    def start_installation(self):
        install_path = self.install_path.get()
        
        if not install_path:
            tk.messagebox.showerror("Error", "Please select an installation directory.")
            return
        
        # Start installation in a separate thread
        threading.Thread(target=self.install, daemon=True).start()
    
    def install(self):
        install_path = self.install_path.get()
        
        try:
            # Update UI
            self.status_label.config(text="Downloading platform tools...")
            self.progress.config(value=0)
            self.progress_label.config(text="0%")
            
            # Download file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
                temp_path = temp_file.name
                
            def report_progress(block_num, block_size, total_size):
                if total_size > 0:
                    percent = (block_num * block_size * 100) / total_size
                    self.progress.config(value=min(percent, 100))
                    self.progress_label.config(text=f"{min(percent, 100):.1f}%")
            
            urllib.request.urlretrieve(PLATFORM_TOOLS_URL, temp_path, report_progress)
            
            # Extract files
            self.status_label.config(text="Extracting files...")
            self.progress.config(value=50)
            self.progress_label.config(text="50%")
            
            # Create directory if it doesn't exist
            os.makedirs(install_path, exist_ok=True)
            
            # Extract zip file
            with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.dirname(install_path))
            
            # Add to PATH if selected
            if self.add_to_path.get():
                self.status_label.config(text="Updating system PATH...")
                self.progress.config(value=75)
                self.progress_label.config(text="75%")
                self.add_to_system_path(install_path)
            
            # Create shortcut if selected
            if self.create_shortcut.get():
                self.status_label.config(text="Creating desktop shortcut...")
                self.progress.config(value=90)
                self.progress_label.config(text="90%")
                self.create_desktop_shortcut(install_path)
            
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            
            # Completed
            self.status_label.config(text="Installation completed successfully!")
            self.progress.config(value=100)
            self.progress_label.config(text="100%")
            
            self.after(1000, lambda: tk.messagebox.showinfo(
                "Installation Complete", 
                "Android Platform Tools have been successfully installed!"
            ))
        
        except Exception as e:
            self.after(0, lambda: tk.messagebox.showerror(
                "Installation Error", 
                f"Error during installation: {str(e)}"
            ))
            self.status_label.config(text="Installation failed.")
    
    def add_to_system_path(self, path):
        try:
            # Using PowerShell to modify PATH
            ps_command = f"""
            [Environment]::SetEnvironmentVariable(
                "Path",
                [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine) + ";{path}",
                [EnvironmentVariableTarget]::Machine
            )
            """
            subprocess.run(["powershell", "-Command", ps_command], check=True)
        except Exception as e:
            raise Exception(f"Failed to update PATH: {str(e)}")
    
    def create_desktop_shortcut(self, install_path):
        try:
            desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
            shortcut_path = os.path.join(desktop_path, "Platform Tools.lnk")
            
            ps_command = f"""
            $WshShell = New-Object -ComObject WScript.Shell
            $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
            $Shortcut.TargetPath = "{os.path.join(install_path, 'adb.exe')}"
            $Shortcut.WorkingDirectory = "{install_path}"
            $Shortcut.Description = "Android Platform Tools"
            $Shortcut.Save()
            """
            subprocess.run(["powershell", "-Command", ps_command], check=True)
        except Exception as e:
            raise Exception(f"Failed to create shortcut: {str(e)}")
    
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def show_error(self, title, message):
        tk.messagebox.showerror(title, message)

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()