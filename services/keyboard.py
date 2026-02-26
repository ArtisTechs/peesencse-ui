import os
import sys
import subprocess
import shutil

_proc = None


def _find_keyboard():
    """Return an executable name/path for a likely on-screen keyboard on the system."""
    # Windows common locations
    if sys.platform.startswith("win"):
        paths = [
            r"C:\Program Files\Common Files\Microsoft Shared\Ink\TabTip.exe",
            r"C:\Windows\System32\osk.exe",
        ]
        for p in paths:
            if os.path.exists(p):
                return p
        return shutil.which("osk.exe") or shutil.which("TabTip.exe")

    # Linux / Raspberry Pi: prefer onboard, matchbox-keyboard, florence
    if sys.platform.startswith("linux"):
        for name in ("onboard", "matchbox-keyboard", "florence"):
            path = shutil.which(name)
            if path:
                return path
        return None

    return None


def show_keyboard():
    """Attempt to open a platform-appropriate on-screen keyboard."""
    global _proc
    if _proc is not None:
        return
    exe = _find_keyboard()
    if not exe:
        return
    try:
        # Start without blocking; detach from parent so it remains open
        _proc = subprocess.Popen([exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        _proc = None


def hide_keyboard():
    """Close common on-screen keyboard processes (cross-platform attempts)."""
    global _proc
    try:
        if sys.platform.startswith("win"):
            subprocess.run(["taskkill", "/IM", "TabTip.exe", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["taskkill", "/IM", "osk.exe", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sys.platform.startswith("linux"):
            # Try pkill for common keyboards
            for name in ("onboard", "matchbox-keyboard", "florence"):
                try:
                    subprocess.run(["pkill", "-f", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception:
                    pass
    except Exception:
        pass
    _proc = None
