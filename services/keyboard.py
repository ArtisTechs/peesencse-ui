import subprocess

_proc = None

def show_keyboard():
    global _proc
    if _proc is None:
        try:
            _proc = subprocess.Popen(["matchbox-keyboard"])
        except Exception:
            _proc = None

def hide_keyboard():
    global _proc
    if _proc:
        _proc.terminate()
        _proc = None