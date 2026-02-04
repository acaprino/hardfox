"""
Build UpdateFirefox.exe from portable_updater.py.

Compiles the standalone updater with PyInstaller as a single-file
windowed executable, reusing the Firefox icon.

Usage:
    python tools/build_portable_updater.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
UPDATER_SCRIPT = SCRIPT_DIR / "portable_updater.py"
OUTPUT_DIR = PROJECT_ROOT / "dist"
ICON_PATH = SCRIPT_DIR / "firefox.ico"


def build_exe():
    """Build UpdateFirefox.exe with PyInstaller."""
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "UpdateFirefox",
        "--distpath", str(OUTPUT_DIR),
        "--workpath", str(PROJECT_ROOT / "build" / "portable_updater"),
        "--specpath", str(PROJECT_ROOT / "build"),
    ]

    if ICON_PATH.exists():
        cmd.extend(["--icon", str(ICON_PATH)])
    else:
        print("Warning: firefox.ico not found. Build the launcher first to extract the icon.")

    cmd.append(str(UPDATER_SCRIPT))

    print("Building UpdateFirefox.exe...")
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    if result.returncode != 0:
        print("Build failed!")
        sys.exit(1)

    exe_path = OUTPUT_DIR / "UpdateFirefox.exe"
    if exe_path.exists():
        print(f"\nBuild successful: {exe_path}")
        print(f"Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
    else:
        print("Build completed but exe not found!")
        sys.exit(1)


def main():
    print("=" * 60)
    print("  Building UpdateFirefox.exe")
    print("=" * 60)

    if not UPDATER_SCRIPT.exists():
        print(f"Error: {UPDATER_SCRIPT} not found")
        sys.exit(1)

    build_exe()

    # Cleanup build artifacts
    build_dir = PROJECT_ROOT / "build" / "portable_updater"
    if build_dir.exists():
        shutil.rmtree(build_dir, ignore_errors=True)
    spec_file = PROJECT_ROOT / "build" / "UpdateFirefox.spec"
    if spec_file.exists():
        spec_file.unlink()

    print("\nDone!")


if __name__ == "__main__":
    main()
