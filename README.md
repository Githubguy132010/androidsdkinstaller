# Android SDK Platform Tools Installer

A user-friendly Windows GUI installer for Android SDK Platform Tools.

![Installer Screenshot](docs/installer_screenshot.png)

## Overview

This installer provides a simple way to set up Android Platform Tools on Windows systems. It handles downloading, extracting, and configuring the platform tools with a modern, intuitive interface.

### Features

- **Modern UI**: Clean, Material Design-inspired interface
- **Custom Installation Directory**: Choose where to install the platform tools
- **PATH Integration**: Option to automatically add platform tools to system PATH
- **Desktop Shortcut**: Create shortcuts for quick access
- **Update Checking**: Verify and download the latest version
- **Progress Tracking**: Visual feedback during installation
- **Admin Privileges**: Properly handles system modifications

## Download

Download the latest version from the [Releases](https://github.com/yourusername/android-sdk-installer/releases) page.

## Requirements

- Windows 10 or newer
- Administrator privileges (required for PATH modification)
- Internet connection (for downloading platform tools)

## Usage

1. Download the installer executable from the Releases page
2. Run the installer with administrator privileges
3. Choose installation options
4. Click "Install" to begin the installation process
5. After completion, platform tools will be available in the installation directory

### Common Tools Included

- `adb` (Android Debug Bridge) - Manage Android devices
- `fastboot` - Flash firmware to devices
- `systrace` - System tracing utility

## Development

### Prerequisites

- Visual Studio 2022 or newer
- .NET 6.0 SDK

### Building from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/android-sdk-installer.git

# Navigate to the project directory
cd android-sdk-installer

# Build the project
dotnet build

# Run the application
dotnet run
```

### Build the Installer

```bash
dotnet publish --configuration Release --self-contained -r win-x64 -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Android is a trademark of Google LLC
- This project is not affiliated with Google or Android