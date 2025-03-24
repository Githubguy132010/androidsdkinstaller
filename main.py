import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import os
import zipfile
from tqdm import tqdm
from threading import Thread
import platform
import subprocess

class AndroidSDKInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Android SDK Platform Tools Installer")
        self.root.geometry("600x400")
        
        # URL for platform-tools
        self.is_windows = platform.system() == "Windows"
        self.platform_tools_url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip" if self.is_windows else "https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
        
        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Installation directory selection
        ttk.Label(main_frame, text="Installation Directory:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.install_path = tk.StringVar(value=os.path.expanduser("~"))
        path_entry = ttk.Entry(main_frame, textvariable=self.install_path, width=50)
        path_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_directory).grid(row=1, column=1, padx=5)

        # Add to PATH option
        self.add_to_path = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Add to System PATH", variable=self.add_to_path).grid(row=2, column=0, sticky=tk.W, pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Status label
        self.status_var = tk.StringVar(value="Ready to install")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)

        # Install button
        self.install_button = ttk.Button(main_frame, text="Install", command=self.start_installation)
        self.install_button.grid(row=5, column=0, columnspan=2, pady=20)

    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir=self.install_path.get())
        if directory:
            self.install_path.set(directory)

    def start_installation(self):
        self.install_button.state(['disabled'])
        self.status_var.set("Starting installation...")
        Thread(target=self.install_platform_tools, daemon=True).start()

    def download_with_progress(self, url, destination):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        
        with open(destination, 'wb') as file, tqdm(
                desc="Downloading",
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
        ) as pbar:
            for data in response.iter_content(block_size):
                size = file.write(data)
                pbar.update(size)
                progress = (pbar.n / total_size) * 100
                self.root.after(0, self.progress.configure, {'value': progress})

    def add_to_system_path(self, path):
        try:
            if self.is_windows:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
                current_path = winreg.QueryValueEx(key, "Path")[0]
                
                if path not in current_path:
                    new_path = current_path + ";" + path if current_path else path
                    winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                    
                winreg.CloseKey(key)
            else:
                # For Linux, modify .bashrc or .zshrc
                shell_rc = os.path.expanduser("~/.bashrc")
                if os.path.exists(os.path.expanduser("~/.zshrc")):
                    shell_rc = os.path.expanduser("~/.zshrc")

                export_line = f'\nexport PATH="$PATH:{path}"'
                with open(shell_rc, 'a+') as rc_file:
                    rc_file.seek(0)
                    if path not in rc_file.read():
                        rc_file.write(export_line)
                
                # Also modify current session's PATH
                os.environ['PATH'] = os.environ.get('PATH', '') + os.pathsep + path
            return True
        except Exception as e:
            return False

    def install_platform_tools(self):
        try:
            install_dir = self.install_path.get()
            platform_tools_dir = os.path.join(install_dir, "platform-tools")
            zip_path = os.path.join(install_dir, "platform-tools.zip")

            # Create directory if it doesn't exist
            os.makedirs(install_dir, exist_ok=True)

            # Download platform-tools
            self.status_var.set("Downloading platform-tools...")
            self.download_with_progress(self.platform_tools_url, zip_path)

            # Extract files
            self.status_var.set("Extracting files...")
            self.progress.configure(value=0)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(install_dir)

            # Set executable permissions on Linux
            if not self.is_windows:
                for root, dirs, files in os.walk(platform_tools_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        os.chmod(file_path, 0o755)

            # Clean up zip file
            os.remove(zip_path)

            # Add to PATH if selected
            if self.add_to_path.get():
                self.status_var.set("Adding to PATH...")
                if self.add_to_system_path(platform_tools_dir):
                    self.status_var.set("Installation completed successfully!")
                else:
                    self.status_var.set("Installation completed, but failed to add to PATH")
            else:
                self.status_var.set("Installation completed successfully!")

            messagebox.showinfo("Success", "Android SDK Platform Tools installed successfully!")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Installation failed: {str(e)}")
        finally:
            self.progress.configure(value=0)
            self.install_button.state(['!disabled'])

if __name__ == "__main__":
    root = tk.Tk()
    app = AndroidSDKInstaller(root)
    root.mainloop()