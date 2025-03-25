from cx_Freeze import setup, Executable
import os
from PyQt5.QtCore import QLibraryInfo

# Get the paths for Qt files
qt_plugins_path = QLibraryInfo.location(QLibraryInfo.PluginsPath)
qt_qml_path = QLibraryInfo.location(QLibraryInfo.Qml2ImportsPath)

# Define the executable and its properties
exe = Executable(
    script="installer.py",
    base="Win32GUI",  # Use Win32GUI to suppress the console window
    target_name="AndroidSDKInstaller.exe",  # Corrected parameter name
    icon=None  # You can specify an icon file here
)

# Define the setup configuration
setup(
    name="Android SDK Platform Tools Installer",
    version="1.0",
    description="A GUI-based installer for Android SDK Platform Tools",
    executables=[exe],
    options={
        "build_exe": {
            "packages": ["os", "sys", "subprocess", "requests", "PyQt5"],
            "include_files": [
                (qt_plugins_path, "plugins"),
                (qt_qml_path, "qml")
            ],  # Include Qt plugins and QML imports
            "include_msvcr": True  # Include Microsoft Visual C++ Redistributable files
        }
    }
)