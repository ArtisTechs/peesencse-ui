import os
import subprocess
import shutil

_proc = None


def _find_tabtip():
    paths = [
        r"C:\Program Files\Common Files\Microsoft Shared\Ink\TabTip.exe",
        r"C:\Windows\System32\osk.exe",
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    # fallback: rely on PATH (osk.exe usually in PATH)
    return shutil.which("osk.exe") or shutil.which("TabTip.exe")


def show_keyboard():
    """Attempt to open the Windows touch keyboard or on-screen keyboard."""
    global _proc
    if _proc is not None:
        return
    exe = _find_tabtip()
    if not exe:
        return
    try:
        # Start without blocking; detach from parent so it remains open
        _proc = subprocess.Popen([exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        _proc = None


def hide_keyboard():
    """Close common on-screen keyboard processes (TabTip.exe / osk.exe)."""
    global _proc
    try:
        subprocess.run(["taskkill", "/IM", "TabTip.exe", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    try:
        subprocess.run(["taskkill", "/IM", "osk.exe", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    _proc = None
