"""Module with code for settings menu."""
import time
import common
from common import Directory


def settings():
    """Menu to change program settings."""
    menu_options = [
        "Add or remove directory", "Change existing directory settings",
        "Change where backups go", "Go back"
    ]
    quit_menu = False
    while not quit_menu:

        common.clear()
        header = common.box("Manage savestates | Settings")
        print(f"{header}\n")
        for i, option in enumerate(menu_options):
            if option == "Go back":
                print("")
            print(f"{str(i + 1)}: {option}")
        print(f"\nChoose an option (1 - {len(menu_options)}): ")
        choice_val = ""
        while not (
                   choice_val.isdigit()
                   and 0 < int(choice_val) <= len(menu_options)
        ):
            choice_val = common.getch()
        choice = menu_options[int(choice_val) - 1]

        if choice == "Add or remove directory":
            add_or_remove_submenu()
        elif choice == "Change existing directory settings":
            change_dir_settings()
        elif choice == "Change where backups go":
            change_backups_destination()
        elif choice == "Go back":
            quit_menu = True


def add_or_remove_submenu():
    """Menu where user can choose to add or remove a directory."""
    menu_options = ["Add directory", "Remove directory", "Go back"]
    quit_menu = False
    while not quit_menu:
        header = common.box("Manage savestates | Settings | Directories")
        common.clear()
        print(f"{header}\n")
        for i, option in enumerate(menu_options):
            if option == "Go back":
                print("")
            print(f"{str(i + 1)}: {option}")
        print(f"\nChoose an option (1 - {len(menu_options)}): ")

        # Wait for user to input a valid value
        choice_val = ""
        while not (choice_val.isdigit() and 0 < int(choice_val) <= len(menu_options)):
            choice_val = common.getch()
        choice = menu_options[int(choice_val) - 1]

        if choice == "Add directory":
            common.add_dir()
        elif choice == "Remove directory":
            remove_dir()
        elif choice == "Go back":
            quit_menu = True


def remove_dir():
    """Prompts user to select a directory, which removes it from pickle
       file list."""
    dirs = common.load_pickle("dirs.txt")
    header = common.box("Manage savestates | Settings | Remove directory")

    common.clear()
    print(f"{header}\n")
    for i, directory in enumerate(dirs):
        print(f"{str(i + 1)}: {directory.path}")
    print(f"\n{str(len(dirs) + 1)}: Go back")
    print(f"\nChoose an option (1 - {len(dirs) + 1}): ")

    # Wait for the user to input a valid value
    choice_val = ""
    while not (choice_val.isdigit() and 0 < int(choice_val) <= len(dirs) + 1):
        choice_val = common.getch()

    # Exit menu if user chooses "Go back"
    if int(choice_val) == len(dirs) + 1:
        return
    
    choice_index = int(choice_val) - 1
    choice = dirs[choice_index]
    print(f"\nThis will stop this program from organizing and backing up {choice.path}")
    print("NOTE: The directory itself is not affected.")
    print("Press \"y\" to confirm. Press any other key to cancel.")
    decision = common.getch()
    # Remove dir from list and redump the pickle
    if "y" in decision:
        del dirs[choice_index]
        common.dump_pickle(dirs, "dirs.txt")
        print(f"\nSuccessfully removed {choice.path} from this program's list")
        time.sleep(1)
    return


def change_dir_settings():
    """Change dir action settings for an existing directory."""
    dirs = common.load_pickle("dirs.txt")
    header = common.box("Manage savestates | Settings | Change directory settings")

    common.clear()
    print(f"{header}\n")
    for i, directory in enumerate(dirs):
        print(f"{str(i + 1)}: {directory.path} (organization style: {directory.action})")
    print(f"\n{str(len(dirs) + 1)}: Go back")
    print(f"\nChoose an option (1 - {len(dirs) + 1}): ")

    # Wait for user to input a valid value
    choice_val = ""
    while not (choice_val.isdigit() and 0 < int(choice_val) <= len(dirs) + 1):
        choice_val = common.getch()

    # Quit if the user chooses "Go back"
    if int(choice_val) == len(dirs) + 1:
        return

    choice_index = int(choice_val) - 1
    choice = dirs[choice_index]
    common.clear()
    print(f"{header}\n")

    # Get new option setting from user
    new_dir_action = common.get_dir_settings(choice.path)

    # Delete directory and re-add it with correct setting
    common.clear()
    new_dir = Directory(choice.path, new_dir_action)
    del dirs[choice_index]
    dirs += [new_dir]
    common.dump_pickle(dirs, "dirs.txt")
    print(f"{header}\n\nSuccessfully changed settings for {choice.path}")
    time.sleep(1)
    return


def change_backups_destination():
    """Change where backups go."""
    backups_directory = common.load_pickle("backups_path.txt")

    header = common.box("Manage savestates | Settings | Change where backups go")
    common.clear()
    print(f"{header}\n\nPlease select a folder to store backups:")
    time.sleep(1)

    # Get the new directory and redump the pickle
    backups_dir_path = common.get_dir_path()
    if backups_dir_path != "":
        common.clear()
        common.dump_pickle(backups_directory, "backups_path.txt")
        print(f"{header}\n\nUpdated backups_dir_path to {backups_dir_path}")
        time.sleep(1)
