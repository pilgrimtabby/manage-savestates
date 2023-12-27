"""Module with code for settings menu."""
import time
from dataclasses import dataclass
import common


@dataclass
class Directory:
    """Stores data about directories organized by directories.organize()."""
    path: str
    action: str


def main():
    """Menu to change program settings."""
    menu_options = ["Add directory", "Remove directory", "Change directory settings",
                    "Change where backups go", "Go back"]
    quit_menu = False
    while not quit_menu:

        header = common.box("Manage savestates | Settings")
        common.clear()
        print(f"{header}\n")
        for i, option in enumerate(menu_options):
            if option == "Go back":
                print("")
            print(f"{str(i + 1)}: {option}")

        user_input = input(f"\nChoose an option (1 - {len(menu_options)}): ")
        if user_input.isdigit() and 0 < int(user_input) <= len(menu_options):
            choice = menu_options[int(user_input) - 1]
            if choice == "Add directory":
                add_dir()
            elif choice == "Remove directory":
                remove_dir()
            elif choice == "Change directory settings":
                change_dir_settings()
            elif choice == "Change where backups go":
                change_backups_destination()
            elif choice == "Go back":
                quit_menu = True
        else:
            print("Not a valid option! Please try again.")
            time.sleep(1)


def add_dir():
    """Prompts user to choose settings for new directory and adds it
    to the directory pickle file."""
    header = common.box("Manage savestates | Settings | Add directory")
    keep_going = True
    while keep_going:
        dirs = common.load_pickle("dirs.txt")
        common.clear()
        print(f"{header}\n\nPlease select a directory:")
        new_dir_path = common.get_dir_path()
        if new_dir_path != "":
            new_dir_action = get_dir_settings(new_dir_path)
            new_dir = Directory(new_dir_path, new_dir_action,)
            dirs += [new_dir]
            common.dump_pickle(dirs, "dirs.txt")
            common.clear()
            print(f"{header}\n\nSuccessfully added:\n{new_dir_path}")
            time.sleep(1)
            user_input = input("\nAdd another directory? Press \"y\" for yes "
                               "(press enter to finish): ").lower()
            if user_input != "y":
                keep_going = False
        else:
            keep_going = False


def remove_dir():
    """Prompts user to select a directory, which removes it from pickle
       file list."""
    header = common.box("Manage savestates | Settings | Remove directory")
    quit_menu = False
    while not quit_menu:
        dirs = common.load_pickle("dirs.txt")
        common.clear()
        print(f"{header}\n")
        if len(dirs) > 0:
            for i, directory in enumerate(dirs):
                print(f"{str(i + 1)}: {directory.path}")
            print(f"\n{str(len(dirs) + 1)}: Go back")

            user_input = input(f"\nChoose a directory, or go back (1 - {len(dirs) + 1}): ")
            if user_input.isdigit() and int(user_input) == len(dirs) + 1:  # "Go back"
                quit_menu = True
            elif user_input.isdigit() and 0 < int(user_input) <= len(dirs):
                choice_index = int(user_input) - 1
                choice_dir = dirs[choice_index]
                common.clear()
                confirmation = input(f"{header}\n\nThis will stop this program from organizing "
                                     f"and backing up:\n{choice_dir.path}\n\n"
                                    "NOTE: The directory itself is not affected.\n"
                                    "Press \"y\" to confirm (press enter to cancel): ").lower()
                if confirmation == "y":
                    del dirs[choice_index]
                    common.dump_pickle(dirs, "dirs.txt")
                    print(f"\nSuccessfully removed {choice_dir.path} from this program's list")
                    time.sleep(1)
                    if len(dirs) == 0:
                        quit_menu = True
            else:
                print("Not a valid option! Please try again.")
                time.sleep(1)
        else:
            print("No directories to remove!")
            time.sleep(1)
            quit_menu = True


def change_dir_settings():
    """Change dir action settings for an existing directory."""
    header = common.box("Manage savestates | Settings | Change directory settings")
    quit_menu = False
    while not quit_menu:
        dirs = common.load_pickle("dirs.txt")
        common.clear()
        print(f"{header}\n")
        if len(dirs) > 0:
            for i, directory in enumerate(dirs):
                if directory.action is not None:
                    print(f"{str(i + 1)}: {directory.path} (setting: {directory.action})")
                else:
                    print(f"{str(i + 1)}: {directory.path} (setting: do nothing)")
            print(f"\n{str(len(dirs) + 1)}: Go back")

            user_input = input(f"\nChoose a directory, or go back (1 - {len(dirs) + 1}): ")
            if user_input.isdigit() and int(user_input) == len(dirs) + 1:  # "Go back"
                quit_menu = True
            elif user_input.isdigit() and 0 < int(user_input) <= len(dirs):
                choice_index = int(user_input) - 1
                choice_dir = dirs[choice_index]

                common.clear()
                print(f"{header}\n")
                choice_dir.action = get_dir_settings(choice_dir.path)

                dirs[choice_index] = choice_dir
                common.dump_pickle(dirs, "dirs.txt")
            else:
                print("Not a valid option! Please try again.")
                time.sleep(1)
        else:
            print("No directories have been added yet!")
            time.sleep(1)
            quit_menu = True


def change_backups_destination():
    """Change where backups go."""
    backups_directory = common.load_pickle("backups_path.txt")
    header = common.box("Manage savestates | Settings | Change where backups go")
    common.clear()
    print(f"{header}\n\nPlease select a folder for storing backups:")
    backups_dir_path = common.get_dir_path()
    if backups_dir_path != "":
        common.dump_pickle(backups_directory, "backups_path.txt")
        print(f"\nUpdated backups_dir_path to:\n{backups_dir_path}")
        time.sleep(2)


def get_dir_settings(dir_path):
    """Gets and returns action settings for a directory (new or old)."""
    header = common.box("Manage savestates | Settings | Directory settings")
    common.clear()
    print(f"{header}\n\nPlease choose an option for files in {dir_path}\n")
    menu_options = ["Trim numbered prefixes from files", "Renumber savestates and macros based on "
                    "their names", "Do not organize"]
    for i, option in enumerate(menu_options):
        print(f"{str(i + 1)}: {option}")
    
    user_input = input(f"\nChoose an option (1 - {len(menu_options)}): ")
    if user_input.isdigit() and 0 < int(user_input) <= len(menu_options):
        choice = menu_options[int(user_input) - 1]
        if choice == "Trim numbered prefixes from files":
            setting = "trim"
        elif choice == "Renumber savestates and macros based on their names":
            setting = "renumber"
        elif choice == "Do not organize":
            setting = None
    else:
        print("Not a valid option! Please try again.")
        time.sleep(1)
    return setting
