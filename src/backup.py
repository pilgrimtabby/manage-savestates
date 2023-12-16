"""Backs up all directories saved in the program to a specified backup directory
   (the directory can be changed in settings)."""
import os
import shutil
import time
import settings
import utilities

def copy_dir():
    """Backs up dir from dir_path to backups_path."""
    dirs = utilities.load_pickle("dirs.txt")
    if dirs == "":
        print("No directories have been added in settings yet! Taking you there...")
        make_new_directories = True
        while make_new_directories:
            old_dirs = utilities.load_pickle("dirs.txt")
            settings.add_dir()
            current_dirs = utilities.load_pickle("dirs.txt")
            if old_dirs == current_dirs:
                if current_dirs == "":
                    return
                break
            print("Add another directory? \"y\" for yes, anything else to continue to backups.")
            decision = utilities.getch()
            if not "y" in decision:
                make_new_directories = False
        dirs = utilities.load_pickle("dirs.txt")
    backups_path = utilities.load_pickle("backups_path.txt")
    if not os.path.exists(backups_path):
        print("Please select a directory to store backups:")
        time.sleep(1)
        backups_path = utilities.get_dir_path()
        if backups_path == "":
            return
        utilities.dump_pickle(backups_path, "backups_path.txt")

    for directory in dirs:
        dir_name = os.path.basename(directory)
        if not os.path.isdir(f"{backups_path}/{dir_name}"):
            os.mkdir(f"{backups_path}/{dir_name}")

        current_datetime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        backed_up_dir_path = f"{backups_path}/{dir_name}/{current_datetime}"
        print(f"Now copying {directory} to {backed_up_dir_path}")
        shutil.copytree(directory, backed_up_dir_path, ignore_dangling_symlinks=True)
        print(f"{dir_name} successfully backed up!")
    print("\nDone! Press any key to return to main menu.")
    utilities.getch()
