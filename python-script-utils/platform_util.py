import sys

def is_windows():
    return sys.platform == "win32"
def is_macos():
    return sys.platform == "darwin"
def is_linux():
    return sys.platform == "linux"