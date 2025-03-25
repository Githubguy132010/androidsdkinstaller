import sys
import os
import subprocess
import requests
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout, QPushButton, QLabel, QCheckBox, QWidget, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt

# Configure logging
logging.basicConfig(
    filename="installer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class InstallerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Android SDK Platform Tools Installer")
        self.setGeometry(100, 100, 600, 400)

        # Main layout
        self.main_layout = QVBoxLayout()

        # Directory selection
        self.install_dir_label = QLabel("Select Installation Directory:")
        self.main_layout.addWidget(self.install_dir_label)

        self.install_dir_button = QPushButton("Choose Directory")
        self.install_dir_button.clicked.connect(self.select_install_directory)
        self.main_layout.addWidget(self.install_dir_button)

        self.selected_dir_label = QLabel("No directory selected")
        self.main_layout.addWidget(self.selected_dir_label)

        # Add to PATH option
        self.add_to_path_checkbox = QCheckBox("Add Platform Tools to System PATH")
        self.main_layout.addWidget(self.add_to_path_checkbox)

        # Install button
        self.install_button = QPushButton("Install")
        self.install_button.clicked.connect(self.start_installation)
        self.main_layout.addWidget(self.install_button)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.main_layout.addWidget(self.progress_bar)

        # Update button
        self.update_button = QPushButton("Check for Updates")
        self.update_button.clicked.connect(self.check_for_updates)
        self.main_layout.addWidget(self.update_button)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def select_install_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Installation Directory")
        if directory:
            self.selected_dir_label.setText(f"Selected Directory: {directory}")
            self.install_dir = directory
        else:
            self.selected_dir_label.setText("No directory selected")

    def start_installation(self):
        try:
            logging.info("Starting installation process.")

            if not hasattr(self, 'install_dir') or not self.install_dir:
                logging.warning("No installation directory selected.")
                QMessageBox.warning(self, "Error", "Please select an installation directory.")
                return

            logging.info(f"Selected installation directory: {self.install_dir}")

            # Simulate installation process
            self.progress_bar.setValue(50)  # Example progress
            logging.info("Installation progress: 50%.")

            if self.add_to_path_checkbox.isChecked():
                logging.info("Adding installation directory to system PATH.")
                self.add_to_system_path(self.install_dir)

            self.progress_bar.setValue(100)
            logging.info("Installation completed successfully.")
            QMessageBox.information(self, "Success", "Installation completed successfully!")
        except Exception as e:
            logging.error(f"Installation failed: {str(e)}")
            QMessageBox.critical(self, "Error", f"Installation failed: {str(e)}")

    def check_for_updates(self):
        try:
            logging.info("Checking for updates.")
            url = "https://developer.android.com/studio/releases/platform-tools"
            response = requests.get(url)
            response.raise_for_status()

            # Simulate parsing the latest version (this would need actual parsing logic)
            latest_version = "34.0.4"  # Example version
            logging.info(f"Latest version found: {latest_version}.")
            QMessageBox.information(self, "Update Checker", f"The latest version is {latest_version}.")
        except requests.RequestException as e:
            logging.error(f"Failed to check for updates: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to check for updates: {str(e)}")

    def add_to_system_path(self, path):
        try:
            subprocess.run(["setx", "PATH", f"%PATH%;{path}"], shell=True, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception("Failed to add to system PATH") from e

if __name__ == "__main__":
    app = QApplication(sys.argv)
    installer = InstallerApp()
    installer.show()
    sys.exit(app.exec_())