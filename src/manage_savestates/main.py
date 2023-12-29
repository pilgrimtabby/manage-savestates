"""Display main menu GUI.

Functions:
    main()
    exit_screen()
"""
import platform
import time

if platform.system() != "Windows":
    import chime

import advanced_cursor
import directories
import settings
import common


def main():
    """Display main menu."""
    menu_options = ["Organize directories", "Back up directories",
                    "Settings", "Quit"]
    quit_menu = False

    while not quit_menu:
        header = common.box("Manage savestates")
        common.clear()
        print(f"{header}\n")
        for i, option in enumerate(menu_options):
            if option == "Quit":
                print("")
            print(f"{str(i + 1)}: {option}")

        user_input = input(f"\nChoose an option (1 - {len(menu_options)}): ")
        if user_input.isdigit() and 0 < int(user_input) <= len(menu_options):
            choice = menu_options[int(user_input) - 1]

            if choice == "Organize directories":
                directories.organize()
            elif choice == "Back up directories":
                directories.back_up()
            elif choice == "Settings":
                settings.main()
            elif choice == "Quit":
                quit_menu = True

        else:
            print("Not a valid option! Please try again.")
            time.sleep(1)

    exit_screen()


def exit_screen():
    """Display splash screen on exit."""
    advanced_cursor.hide()
    if platform.system() != "Windows":
        chime.theme("mario")
        chime.info()
    common.clear()
    print("\n\n\n               Come again soon!\n\n\n"
        "               ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇\n"
        "               ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⢿⡿⢿⣿⣿⣿⠃\n"
        "               ⣿⣿⣿⣿⣿⣿⣥⣄⣀⣀⠀⠀⠀⠀⠀⢰⣾⣿⣿⠏\n"
        "               ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣜⡻⠋\n"
        "               ⣿⣿⡿⣿⣿⣿⣿⠿⠿⠟⠛⠛⠛⠋⠉⠉⢉⡽⠃\n"
        "               ⠉⠛⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⡤⠚⠉\n"
        "               ⣿⠉⠛⢶⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⡇\n"
        "               ⠟⠃⠀⠀⠀⠈⠲⣴⣦⣤⣤⣤⣶⡾⠁\n\n")
    time.sleep(.5)
    common.clear()
    advanced_cursor.show()


if __name__ == "__main__":
    main()
