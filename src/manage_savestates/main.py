"""Display user menu that allows user to back up organize directories,
   back up directories, change settings, or quit.
"""
import cursor
import backup
import organize
import settings
import common


def main():
    """Display main menu."""
    menu_options = ["Organize directories", "Back up directories",
                    "Settings", "Quit"]
    cursor.hide()
    quit_menu = False

    while not quit_menu:
        common.clear()
        header = common.box("Manage savestates")
        print(f"{header}\n")
        for i, option in enumerate(menu_options):
            if option == "Quit":
                print("")
            print(f"{str(i + 1)}: {option}")
        print(f"\nChoose an option (1 - {len(menu_options)}): ")

        choice_val = ""
        while not (choice_val.isdigit()
                   and 0 < int(choice_val) <= len(menu_options)):
            choice_val = common.getch()
        choice = menu_options[int(choice_val) - 1]

        if choice == "Organize directories":
            organize.organize()
        elif choice == "Back up directories":
            backup.copy_dir()
        elif choice == "Settings":
            settings.settings()
        elif choice == "Quit":
            quit_menu = common.exit_screen(quit_menu)
            cursor.show()
