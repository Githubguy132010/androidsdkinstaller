from cx_Freeze import setup, Executable
import PyQt5.QtCore

# Function to get Qt paths
def get_qt_paths():
    try:
        from cx_Freeze.hooks import qt_paths
        return qt_paths()
    except KeyError as e:
        if str(e) == "'QmlImportsPath'":
            return {}
        raise

qt_paths = get_qt_paths()

# Your existing setup code
setup(
    name="Android SDK Installer",
    version="1.0",
    description="Installer for Android SDK Platform Tools",
    options={
        "build_exe": {
            "include_files": qt_paths.get("QmlImportsPath", ""),
        }
    },
    executables=[Executable("main.py")]
)