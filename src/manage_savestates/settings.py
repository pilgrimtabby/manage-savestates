"""Display settings menu GUI.

Classes:
    GZDirectory(path: str, action: str)

Functions:
    main()
    add_dir()
    remove_dir()
    change_dir_settings()
    set_dir_settings(dir_path: str) -> str | None
    change_backups_destination()
"""
import time
from dataclasses import dataclass
import common


@dataclass
class GZDirectory:
    """Store information about a directory acted on by this program.
    
    Attributes:
        path (str): Absolute path to the directory.
        action (str | None): How the directory is organized.
            `trim`: Remove numbered prefixes from files
            `renumber`: Number files in order from 000 to 999.
            `None`: No action taken. Can still be backed up.

            See directories.py documentation / README.md for more info.
    """
    path: str
    action: str


def main():
    """Display settings menu GUI."""
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
                add_gzdir()
            elif choice == "Remove directory":
                remove_gzdir()
            elif choice == "Change directory settings":
                change_gzdir_settings()
            elif choice == "Change where backups go":
                change_backups_destination()
            elif choice == "Go back":
                quit_menu = True
        else:
            print("Not a valid option! Please try again.")
            time.sleep(1)


def add_gzdir():
    """Add new directory to directories pickle (pickles/gzdirs.txt)."""
    header = common.box("Manage savestates | Settings | Add directory")
    keep_going = True
    while keep_going:
        gzdirs = common.load_pickle("gzdirs.txt")
        common.clear()
        print(f"{header}\n\nPlease select a directory:")
        new_gzdir_path = common.get_file_path(file_type="dir")

        if new_gzdir_path != "":
            for gzdir in gzdirs:
                if new_gzdir_path == gzdir.path:
                    print("Error: You've already added this directory!")
                    time.sleep(2)
                    break
            else:
                new_gzdir = GZDirectory(new_gzdir_path, "")
                new_gzdir.action = set_gzdir_settings(new_gzdir)
                gzdirs += [new_gzdir]
                common.dump_pickle(gzdirs, "gzdirs.txt")
                common.clear()
                print(f"{header}\n\nSuccessfully added:\n{new_gzdir_path}")
                time.sleep(1)

            user_input = input("\nAdd another directory? Press \"y\" for yes "
                               "(press enter to finish): ").lower()
            if user_input != "y":
                keep_going = False

        else:
            keep_going = False


def remove_gzdir():
    """Remove directory from directories pickle (pickles/gzdirs.txt)."""
    header = common.box("Manage savestates | Settings | Remove directory")
    quit_menu = False
    while not quit_menu:
        gzdirs = common.load_pickle("gzdirs.txt")
        common.clear()
        print(f"{header}\n")
        if len(gzdirs) > 0:
            for i, gzdirectory in enumerate(gzdirs):
                print(f"{str(i + 1)}: {gzdirectory.path}")
            print(f"\n{str(len(gzdirs) + 1)}: Go back")

            user_input = input(f"\nChoose a directory, or go back (1 - {len(gzdirs) + 1}): ")
            if user_input.isdigit() and int(user_input) == len(gzdirs) + 1:  # "Go back"
                quit_menu = True
            elif user_input.isdigit() and 0 < int(user_input) <= len(gzdirs):
                choice_index = int(user_input) - 1
                choice_gzdir = gzdirs[choice_index]
                common.clear()
                confirmation = input(f"{header}\n\nThis will stop this program from organizing "
                                     f"and backing up:\n{choice_gzdir.path}\n\n"
                                     "NOTE: The directory itself is not affected.\n"
                                     "Press \"y\" to confirm (press enter to cancel): ").lower()
                if confirmation == "y":
                    del gzdirs[choice_index]
                    common.dump_pickle(gzdirs, "gzdirs.txt")
                    print(f"\nSuccessfully removed {choice_gzdir.path} from this program's list")
                    time.sleep(1)
                    if len(gzdirs) == 0:
                        quit_menu = True
            else:
                print("Not a valid option! Please try again.")
                time.sleep(1)
        else:
            print("No directories to remove!")
            time.sleep(1)
            quit_menu = True


def change_gzdir_settings():
    """Print / allow changes to dir.action for existing directories."""
    header = common.box("Manage savestates | Settings | Change directory settings")
    quit_menu = False
    while not quit_menu:
        gzdirs = common.load_pickle("gzdirs.txt")
        common.clear()
        print(f"{header}\n")
        if len(gzdirs) > 0:
            for i, gzdirectory in enumerate(gzdirs):
                if gzdirectory.action is not None:
                    print(f"{str(i + 1)}: {gzdirectory.path} (setting: {gzdirectory.action})")
                else:
                    print(f"{str(i + 1)}: {gzdirectory.path} (setting: do nothing)")
            print(f"\n{str(len(gzdirs) + 1)}: Go back")

            user_input = input(f"\nChoose a directory, or go back (1 - {len(gzdirs) + 1}): ")
            if user_input.isdigit() and int(user_input) == len(gzdirs) + 1:  # "Go back"
                quit_menu = True
            elif user_input.isdigit() and 0 < int(user_input) <= len(gzdirs):
                choice_index = int(user_input) - 1
                choice_gzdir = gzdirs[choice_index]

                common.clear()
                print(f"{header}\n")
                choice_gzdir.action = set_gzdir_settings(choice_gzdir)

                gzdirs[choice_index] = choice_gzdir
                common.dump_pickle(gzdirs, "gzdirs.txt")
            else:
                print("Not a valid option! Please try again.")
                time.sleep(1)
        else:
            print("No directories have been added yet!")
            time.sleep(1)
            quit_menu = True


def set_gzdir_settings(directory):
    """Prompt user to enter new dir.action for a directory at `path`.

    Args:
        directory (GZDirectory object): Object whose .path attribute is
            to be modified.
    
    Returns:
        setting (str | None): How the directory is organized.
            `trim`: Remove numbered prefixes from files
            `renumber`: Number files in order from 000 to 999.
            `None`: No action taken. Can still be backed up.

            See directories.py documentation / README.md for more info
            on these settings.
    """
    header = common.box("Manage savestates | Settings | Directory settings")
    common.clear()
    print(f"{header}\n\nPlease choose an option for files in {directory.path}\n")
    menu_options = ["Trim numbered prefixes from files", "Renumber savestates and macros based on "
                    "their names", "Do not organize"]
    for i, option in enumerate(menu_options):
        print(f"{str(i + 1)}: {option}")

    user_input = input(f"\nChoose an option (1 - {len(menu_options)}): ")
    if user_input.isdigit() and 0 < int(user_input) <= len(menu_options):
        choice = menu_options[int(user_input) - 1]
        if choice == "Trim numbered prefixes from files":
            return "trim"
        if choice == "Renumber savestates and macros based on their names":
            return "renumber"
        if choice == "Do not organize":
            return None
    else:
        print("Not a valid option! Please try again.")
        time.sleep(1)


def change_backups_destination():
    """Change where directories.back_up() copies files."""
    backups_directory = common.load_pickle("backups_path.txt")
    header = common.box("Manage savestates | Settings | Change where backups go")
    common.clear()
    print(f"{header}\n\nPlease select a folder for storing backups:")
    backups_dir_path = common.get_file_path(file_type="dir")
    if backups_dir_path != "":
        gzdirs = common.load_pickle("gzdirs.txt")
        for gzdir in gzdirs:
            if gzdir.path == backups_dir_path:
                print("Error: You can't store backups in a folder you're backing up.")
                time.sleep(2)
                break
        else:
            common.dump_pickle(backups_dir_path, "backups_path.txt")
            print(f"\nUpdated backups storage folder to:\n{backups_dir_path}")
            time.sleep(2)
