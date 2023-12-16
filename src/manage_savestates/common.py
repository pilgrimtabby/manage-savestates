"""Supplementary functions for manage-savestates used by more than one module."""
import os
import pickle
import platform
import subprocess
import sys
import termios
import time
import tkinter
import tkinter.filedialog
import tty
from dataclasses import dataclass
import chime
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


def add_dir():
    """Prompts user to choose settings for new directory and adds it
       to the directory pickle file."""
    dirs = load_pickle("dirs.txt")
    header = box("Manage savestates | Settings | Add directory")
    clear()
    print(f"{header}\n\nPlease select the directory you want to add:")
    time.sleep(1)
    new_dir_path = get_dir_path()
    clear()
    print(f"{header}\n")
    # save settings for the new dir and add them to the dirs.txt pickle file
    if new_dir_path != "":
        new_dir_action = get_dir_settings(new_dir_path)
        new_dir = Directory(new_dir_path, new_dir_action,)
        dirs += [new_dir]
        dump_pickle(dirs, "dirs.txt")
        clear()
        print(f"{header}\n\nSuccessfully added new directory {new_dir_path}")
        time.sleep(1)


def exit_screen(quit_menu):
    """Shows splash screen when program is exiting."""
    chime.theme("mario")
    chime.info()
    clear()
    print("\n\n\n                    Come again!\n\n\n"
        "               ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇\n"
        "               ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⢿⡿⢿⣿⣿⣿⠃\n"
        "               ⣿⣿⣿⣿⣿⣿⣥⣄⣀⣀⠀⠀⠀⠀⠀⢰⣾⣿⣿⠏\n"
        "               ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣜⡻⠋\n"
        "               ⣿⣿⡿⣿⣿⣿⣿⠿⠿⠟⠛⠛⠛⠋⠉⠉⢉⡽⠃\n"
        "               ⠉⠛⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⡤⠚⠉\n"
        "               ⣿⠉⠛⢶⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⡇\n"
        "               ⠟⠃⠀⠀⠀⠈⠲⣴⣦⣤⣤⣤⣶⡾⠁\n\n")
    time.sleep(.5)
    clear()

    quit_menu = True
    return quit_menu


def get_dir_settings(dir_path):
    """Gets and returns action settings for a directory (new or old)."""
    print(f"Please choose an option for files in {dir_path}\n")
    menu_options = [
        "Trim numbered prefixes from files",
        "Renumber savestates and macros based on their names",
        "Do not organize",
    ]
    for i, option in enumerate(menu_options):
        print(f"{str(i + 1)}: {option}")
    choice_val = ""
    while not (
               choice_val.isdigit()
               and 0 < int(choice_val) <= len(menu_options)
    ):
        choice_val = getch()
    choice = menu_options[int(choice_val) - 1]
    if choice == "Trim numbered prefixes from files":
        setting = "trim"
    if choice == "Renumber savestates and macros based on their names":
        setting = "reorder"
    if choice == "Do not organize":
        setting = None
    print(f"\nChoice: {setting}")
    time.sleep(1)
    return setting


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
    tkinter.Tk().withdraw()  # Prevents empty tkinter window from appearing
    dir_path = tkinter.filedialog.askdirectory()
    focus_window()
    return dir_path


def get_file_path():
    """Brings up a window that allows user to select a file."""
    tkinter.Tk().withdraw()  # Prevents empty tkinter window from appearing
    file_path = tkinter.filedialog.askopenfilename()
    focus_window()
    return file_path


def getch():
    """Accepts and returns exactly one character of input without needing
       to press enter."""
    if platform.system() == "Windows":
        return msvcrt.getwch()
    fdd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fdd)
    try:
        tty.setraw(sys.stdin.fileno())
        chh = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fdd, termios.TCSADRAIN, old_settings)
    return chh


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


def no_dirs_edge_case_handling():
    """Handles case where no directories have been selected for backing up/ organizing yet."""
    print("No directories have been added in settings yet! Taking you there...")
    make_new_directories = True
    while make_new_directories:
        old_dirs = load_pickle("dirs.txt")
        add_dir()
        current_dirs = load_pickle("dirs.txt")
        if old_dirs == current_dirs:
            break  # quit if the user hits cancel in the popup window
        print("Add another directory? \"y\" for yes, anything else to continue.")
        decision = getch()
        if not "y" in decision:
            make_new_directories = False
