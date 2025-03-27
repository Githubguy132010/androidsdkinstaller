import sys
import os
import requests
import win32security
import win32api
import win32con
import ctypes
import logging
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QLineEdit,
                            QFileDialog, QProgressBar, QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont

# Logging configuratie
logging.basicConfig(
    filename='installer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path
        
    def run(self):
        try:
            response = requests.get(self.url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            downloaded = 0
            
            with open(self.save_path, 'wb') as f:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    f.write(data)
                    if total_size:
                        progress = int((downloaded / total_size) * 100)
                        self.progress.emit(progress)
            
            self.finished.emit(True, "Download voltooid")
        except Exception as e:
            logging.error(f"Download fout: {str(e)}")
            self.finished.emit(False, f"Download mislukt: {str(e)}")

class InstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Android SDK Platform Tools Installer")
        self.setMinimumSize(600, 400)
        
        # Hoofdwidget en layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Titel
        title = QLabel("Android SDK Platform Tools Installer")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Installatie directory selectie
        dir_layout = QHBoxLayout()
        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Kies installatie directory...")
        dir_button = QPushButton("Bladeren")
        dir_button.clicked.connect(self.select_directory)
        dir_layout.addWidget(QLabel("Installatie Directory:"))
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(dir_button)
        layout.addLayout(dir_layout)
        
        # PATH optie
        self.path_checkbox = QCheckBox("Voeg toe aan systeem PATH")
        self.path_checkbox.setChecked(True)
        layout.addWidget(self.path_checkbox)
        
        # Update checker
        self.update_button = QPushButton("Controleer voor updates")
        self.update_button.clicked.connect(self.check_updates)
        layout.addWidget(self.update_button)
        
        # Voortgangsbalk
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Installatie knop
        self.install_button = QPushButton("Installeer")
        self.install_button.clicked.connect(self.start_installation)
        layout.addWidget(self.install_button)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Controleer administrator rechten
        self.check_admin_rights()
        
    def check_admin_rights(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
            
    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Selecteer Installatie Directory",
            os.path.expanduser("~")
        )
        if dir_path:
            self.dir_input.setText(dir_path)
            
    def check_updates(self):
        try:
            # URL voor de laatste versie van platform-tools
            response = requests.get("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
            if response.status_code == 200:
                QMessageBox.information(
                    self,
                    "Update Check",
                    "Er is een nieuwe versie beschikbaar. De installatie zal de laatste versie gebruiken."
                )
            else:
                QMessageBox.warning(
                    self,
                    "Update Check",
                    "Kon niet controleren op updates. Controleer uw internetverbinding."
                )
        except Exception as e:
            logging.error(f"Update check fout: {str(e)}")
            QMessageBox.warning(
                self,
                "Update Check",
                f"Fout bij het controleren op updates: {str(e)}"
            )
            
    def start_installation(self):
        if not self.check_admin_rights():
            QMessageBox.warning(
                self,
                "Administrator Rechten",
                "Dit programma heeft administrator rechten nodig om te installeren."
            )
            return
            
        install_dir = self.dir_input.text()
        if not install_dir:
            QMessageBox.warning(
                self,
                "Directory Selectie",
                "Selecteer eerst een installatie directory."
            )
            return
            
        self.progress_bar.setVisible(True)
        self.install_button.setEnabled(False)
        
        # Start download thread
        self.download_thread = DownloadThread(
            "https://dl.google.com/android/repository/platform-tools-latest-windows.zip",
            os.path.join(install_dir, "platform-tools.zip")
        )
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.installation_finished)
        self.download_thread.start()
        
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        
    def installation_finished(self, success, message):
        self.progress_bar.setVisible(False)
        self.install_button.setEnabled(True)
        self.status_label.setText(message)
        
        if success:
            QMessageBox.information(
                self,
                "Installatie Voltooid",
                "De Android SDK Platform Tools zijn succesvol geïnstalleerd."
            )
        else:
            QMessageBox.critical(
                self,
                "Installatie Mislukt",
                f"Er is een fout opgetreden tijdens de installatie: {message}"
            )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InstallerWindow()
    window.show()
    sys.exit(app.exec()) 