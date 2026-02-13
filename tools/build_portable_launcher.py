"""
Build MyFox.exe from portable_launcher.c.

Extracts the Firefox icon from firefox.exe and compiles the C launcher
with Zig CC as a tiny native Windows executable (~20 KB).

Usage:
    python tools/build_portable_launcher.py

Requirements:
    pip install pillow   (optional, for icon extraction)
    Zig compiler on PATH, or auto-detected from Nuitka cache
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
LAUNCHER_SRC = SCRIPT_DIR / "portable_launcher.c"
OUTPUT_DIR = PROJECT_ROOT / "dist"


def find_zig() -> str:
    """Find Zig compiler: PATH first, then Nuitka's cached download."""
    # Check PATH
    for path_dir in os.environ.get("PATH", "").split(os.pathsep):
        zig = Path(path_dir) / "zig.exe"
        if zig.is_file():
            return str(zig)

    # Check Nuitka cache
    nuitka_cache = Path.home() / "AppData" / "Local" / "Nuitka" / "Nuitka" / "Cache" / "downloads"
    for zig_exe in nuitka_cache.rglob("zig.exe"):
        return str(zig_exe)

    return None


def extract_firefox_icon(output_ico: Path) -> bool:
    """Extract icon from firefox.exe using PowerShell."""
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("Pillow not installed, skipping icon extraction.")
        return False

    ff_paths = [
        Path(r"C:\Program Files\Mozilla Firefox\firefox.exe"),
        Path(r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"),
    ]
    ff_exe = None
    for p in ff_paths:
        if p.exists():
            ff_exe = str(p)
            break

    if not ff_exe:
        print("Firefox not found, trying VisualElements PNG fallback...")
        return _icon_from_png(output_ico)

    return _extract_icon_powershell(ff_exe, output_ico)


def _extract_icon_powershell(exe_path: str, output_ico: Path) -> bool:
    """Extract icon from exe using PowerShell with encoded command."""
    import base64

    with tempfile.TemporaryDirectory() as tmpdir:
        png_path = Path(tmpdir) / "icon.png"
        exe_path_safe = exe_path.replace("\\", "/")
        png_path_safe = str(png_path).replace("\\", "/")
        ps_script = (
            "Add-Type -AssemblyName System.Drawing\n"
            f"$icon = [System.Drawing.Icon]::ExtractAssociatedIcon('{exe_path_safe}')\n"
            "$bmp = $icon.ToBitmap()\n"
            f"$bmp.Save('{png_path_safe}', [System.Drawing.Imaging.ImageFormat]::Png)\n"
        )
        encoded = base64.b64encode(ps_script.encode("utf-16-le")).decode("ascii")
        result = subprocess.run(
            ["powershell", "-NoProfile", "-EncodedCommand", encoded],
            capture_output=True, text=True
        )
        if result.returncode != 0 or not png_path.exists():
            print(f"PowerShell icon extraction failed: {result.stderr}")
            return _icon_from_png(output_ico)

        return _png_to_ico(png_path, output_ico)


def _icon_from_png(output_ico: Path) -> bool:
    """Create icon from Firefox VisualElements PNG."""
    png_path = Path(r"C:\Program Files\Mozilla Firefox\browser\VisualElements\VisualElements_150.png")
    if not png_path.exists():
        print(f"PNG fallback not found at {png_path}")
        return False
    return _png_to_ico(png_path, output_ico)


def _png_to_ico(png_path: Path, output_ico: Path) -> bool:
    """Convert a PNG to a multi-size ICO file."""
    try:
        from PIL import Image
        img = Image.open(png_path)
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        output_ico.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_ico), format="ICO", sizes=sizes)
        print(f"Icon saved: {output_ico}")
        return True
    except Exception as e:
        print(f"PNG to ICO conversion failed: {e}")
        return False


def build_exe(icon_path: Path = None):
    """Build MyFox.exe with Zig CC."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    zig = find_zig()
    if not zig:
        print("ERROR: Zig compiler not found.")
        print("Install Zig (https://ziglang.org/download/) or run:")
        print("  pip install ziglang")
        sys.exit(1)

    print(f"Using Zig: {zig}")

    exe_path = OUTPUT_DIR / "MyFox.exe"

    cmd = [
        zig, "cc",
        "-target", "x86_64-windows-gnu",
        "-Os",
        "-municode",
        str(LAUNCHER_SRC),
        "-lshlwapi", "-lkernel32", "-luser32",
        "-o", str(exe_path),
        "-Wl,--subsystem,windows",
    ]

    # Embed icon via .rc resource file if available
    rc_path = None
    ico_copy = None
    if icon_path and icon_path.exists():
        # Copy .ico next to the .c source and use relative path in .rc
        ico_copy = LAUNCHER_SRC.parent / "launcher_icon.ico"
        import shutil
        shutil.copy2(icon_path, ico_copy)
        rc_path = SCRIPT_DIR / "launcher.rc"
        rc_path.write_text('1 ICON "launcher_icon.ico"\n', encoding="utf-8")
        cmd.append(str(rc_path))

    print("Compiling portable_launcher.c...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Cleanup temp files
    if rc_path and rc_path.exists():
        rc_path.unlink()
    if ico_copy and ico_copy.exists():
        ico_copy.unlink()

    if result.returncode != 0:
        print(f"Build failed!\n{result.stderr}")
        # If icon embedding failed, retry without it
        if rc_path and icon_path:
            print("Retrying without icon...")
            cmd = [c for c in cmd if c != str(rc_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Build failed!\n{result.stderr}")
                sys.exit(1)
            else:
                print("Built without icon.")
        else:
            sys.exit(1)

    if exe_path.exists():
        size_kb = exe_path.stat().st_size / 1024
        print(f"\nBuild successful: {exe_path}")
        print(f"Size: {size_kb:.0f} KB")
    else:
        print("Build completed but exe not found!")
        sys.exit(1)


def main():
    print("=" * 60)
    print("  Building MyFox.exe (native C)")
    print("=" * 60)

    # Step 1: Extract icon (skip if already exists)
    icon_path = SCRIPT_DIR / "firefox.ico"
    if icon_path.exists():
        print(f"\n[1/2] Using existing icon: {icon_path}")
    else:
        print("\n[1/2] Extracting Firefox icon...")
        if not extract_firefox_icon(icon_path):
            print("Warning: Could not extract icon, building without icon.")
            icon_path = None

    # Step 2: Build exe
    print("\n[2/2] Compiling launcher...")
    build_exe(icon_path)

    print("\nDone!")


if __name__ == "__main__":
    main()
