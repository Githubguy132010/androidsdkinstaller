# Android SDK Platform Tools Installer

A simple GUI installer for Android SDK Platform Tools that makes it easy to install ADB, Fastboot, and other Android platform tools on Windows.

## Features

- Easy-to-use graphical interface
- Automatic download of the latest Android SDK Platform Tools
- Option to add platform tools to system PATH
- Silent installation support
- Clean uninstallation option
- Progress tracking during installation

## Download

Download the latest installer from the [Releases](../../releases) page.

## Usage

1. Download the `AndroidSDKInstaller.exe` from the latest release
2. Run the installer
3. Choose your installation directory
4. Select whether to add Platform Tools to your system PATH
5. Click "Install" to complete the installation

After installation, you can use ADB, Fastboot, and other Android Platform Tools from any terminal window.

## Building from Source

### Prerequisites

- Python 3.10 or higher
- Required Python packages (install using `pip install -r requirements.txt`):
  - requests
  - tqdm
  - python-dotenv
  - pyinstaller

### Build Steps

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Build the executable:
   ```
   pyinstaller --name="AndroidSDKInstaller" --windowed --onefile --icon="icon.ico" main.py
   ```

The built executable will be available in the `dist` directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Android SDK Platform Tools by Google
- PyInstaller for enabling executable creation
- All contributors to this project