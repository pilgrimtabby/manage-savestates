"""Supplementary functions."""
import os
import pickle
import platform
import subprocess
import tkinter
import tkinter.filedialog

if platform.system() == "Windows":
    import win32ui


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


def focus_window(window=None):
    """Bring this program's window into focus."""
    if platform.system() == "Windows":
        if window is not None:
            window.SetForegroundWindow()
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
    if platform.system() == "Windows":
        program_window = win32ui.GetForegroundWindow()
    else:
        program_window = None
    tkinter.Tk().withdraw()  # Prevents empty tkinter window from appearing
    dir_path = tkinter.filedialog.askdirectory()
    focus_window(program_window)
    return dir_path


def get_file_path():
    """Brings up a window that allows user to select a file."""
    if platform.system() == "Windows":
        program_window = win32ui.GetForegroundWindow()
    else:
        program_window = None
    tkinter.Tk().withdraw()  # Prevents empty tkinter window from appearing
    file_path = tkinter.filedialog.askopenfilename()
    focus_window(program_window)
    return file_path


def load_pickle(file_name):
    """Return data (dict or string) from a pickle file."""
    program_dir_path = os.path.dirname(os.path.realpath(__file__))
    # Create the pickles directory if it doesn't exists yet
    if not os.path.isdir(f"{program_dir_path}/pickles"):
        os.mkdir(f"{program_dir_path}/pickles")
    # Create the pickle file with an empty list if it doesn't exist yet
    if not os.path.exists(f"{program_dir_path}/pickles/{file_name}"):
        dump_pickle([], file_name)
    # Read the pickle file
    with open(f"{program_dir_path}/pickles/{file_name}", "rb") as file:
        return pickle.load(file)
