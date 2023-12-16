"""Display user menu that allows user to back up organize directories,
   back up directories, change settings, or quit.
"""
import time
import chime
import cursor
import organize
import settings
import utilities
from utilities import Directory


def main():
    """Display main menu."""
    menu_options = ["Organize directories", "Back up directories",
                    "Settings", "Quit"]
    cursor.hide()
    quit_menu = False

    while not quit_menu:
        utilities.clear()
        header = utilities.box("Manage savestates")
        print(f"{header}\n")
        for i, option in enumerate(menu_options):
            print(f"{str(i + 1)}: {option}")
        print(f"\nChoose an option (1 - {len(menu_options)}): ")

        choice_val = ""
        while not (choice_val.isdigit()
                   and 0 < int(choice_val) <= len(menu_options)):
            choice_val = utilities.getch()
        choice = menu_options[int(choice_val) - 1]

        if choice == "Organize directories":
            organize.organize()
        elif choice == "Back up GZ folder":
            organize.back_up_gz()
        elif choice == "Settings":
            settings.settings()
        elif choice == "Quit":
            quit_menu = exit_screen(quit_menu)


def exit_screen(quit_menu):
    """Shows splash screen when program is exiting."""
    chime.theme("mario")
    chime.info()
    utilities.clear()
    print("\n\n\n                   Exiting Pog\n\n\n"
        "               ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇\n"
        "               ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⢿⡿⢿⣿⣿⣿⠃\n"
        "               ⣿⣿⣿⣿⣿⣿⣥⣄⣀⣀⠀⠀⠀⠀⠀⢰⣾⣿⣿⠏\n"
        "               ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣜⡻⠋\n"
        "               ⣿⣿⡿⣿⣿⣿⣿⠿⠿⠟⠛⠛⠛⠋⠉⠉⢉⡽⠃\n"
        "               ⠉⠛⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⡤⠚⠉\n"
        "               ⣿⠉⠛⢶⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⡇\n"
        "               ⠟⠃⠀⠀⠀⠈⠲⣴⣦⣤⣤⣤⣶⡾⠁\n\n")
    time.sleep(.5)
    cursor.show()
    utilities.clear()

    quit_menu = True
    return quit_menu


main()
