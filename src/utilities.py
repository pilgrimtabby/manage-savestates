"""Supplementary functions for manage-savestates used by more than one module."""
import os
import pickle
import platform
import subprocess
import sys
import termios
import tkinter
import tkinter.filedialog
import tty
from dataclasses import dataclass
try: # importing Windows-only module
    import msvcrt
    import win32gui
except ImportError:
    pass


@dataclass
class Directory:
    """Stores data about directories organized by organize_gz()."""
    path: str
    action: str


def box(txt):
    """Wraps text inside a decorative box and returns the box."""
    txt = str(txt)

    side = "+"
    for _ in range(len(txt) + 4):
        side += "-"
    side += "+"

    middle = f"|  {txt}  |"

    boxed_text = f"{side}\n{middle}\n{side}"
    return boxed_text


def clear():
    """Clear screen and put cursor at top."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def dump_pickle(user_data, file_name):
    """Dump user data (dict or list) into a pickle file."""
    program_dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f"{program_dir_path}/pickles/{file_name}", "wb") as file:
        pickle.dump(user_data, file)
        file.close()


def focus_window():
    """Bring this program's window into focus."""
    if platform.system() == "Windows":
        hwnd = win32gui.FindWindowEx(0,0,0, "C:\\Windows\\py.exe")
        win32gui.SetForegroundWindow(hwnd)
    else:
        # Applescript that finds the correct terminal window and activates it.
        # This code can be adjusted to work with other programs by changing the word
        # in quotes on line that says "set hw to windows whose contents...".
        script = '''
            tell application "Terminal"
                activate
                set hw to windows whose contents contains "main.py"
                --> {window id 67 of application "Terminal"}
                set hw1 to item 1 of hw
                --> window id 67 of application "Terminal"
                set index of hw1 to 1
            end tell'''
        subprocess.run(["osascript", "-e", script], check=False)


def get_dir_path():
    """Brings up a window that allows user to select a directory."""
    tkinter.Tk().withdraw() # Prevents empty tkinter window from appearing
    dir_path = tkinter.filedialog.askdirectory()
    focus_window()
    return dir_path


def get_file_path():
    """Brings up a window that allows user to select a file."""
    tkinter.Tk().withdraw() # Prevents empty tkinter window from appearing
    file_path = tkinter.filedialog.askopenfilename()
    focus_window()
    return file_path


def getch():
    """Accepts and returns exactly one character of input without needing
       to press enter."""
    if platform.system() == "Windows":
        return msvcrt.getwch()
    old_settings = termios.tcgetattr(sys.stdin.fileno())
    try:
        tty.setraw(sys.stdin.fileno())
    finally:
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)
    return sys.stdin.read(1)


def load_pickle(file_name):
    """Return data (dict or string) from a pickle file."""
    program_dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f"{program_dir_path}/pickles/{file_name}", "rb") as file:
        return pickle.load(file)
