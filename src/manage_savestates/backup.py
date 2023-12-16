"""Backs up all directories saved in the program to a specified backup directory
   (the directory can be changed in settings)."""
import os
import shutil
import time
import utilities

def copy_dir():
    """Backs up dir from dir_path to backups_path."""
    dirs = utilities.load_pickle("dirs.txt")
    if dirs == []:
        utilities.no_dirs_edge_case_handling()
        dirs = utilities.load_pickle("dirs.txt")
        if dirs == []:
            return
    backups_path = utilities.load_pickle("backups_path.txt")
    header = utilities.box("Manage savestates | Back up directories")

    if backups_path == [] or not os.path.exists(backups_path):
        utilities.clear()
        print(f"{header}\n\nPlease select a directory to store backups:")
        time.sleep(1)
        backups_path = utilities.get_dir_path()
        if backups_path == "":
            return
        utilities.dump_pickle(backups_path, "backups_path.txt")

    utilities.clear()
    print(f"{header}\n")
    for directory in dirs:
        dir_name = os.path.basename(directory.path)
        if not os.path.isdir(f"{backups_path}/{dir_name}"):
            os.mkdir(f"{backups_path}/{dir_name}")

        current_datetime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        backed_up_dir_path = f"{backups_path}/{dir_name}/{current_datetime}"
        header = utilities.box("Manage savestates | Back up directories")
        print(f"Now copying\n{directory.path} to\n{backed_up_dir_path}")
        shutil.copytree(directory.path, backed_up_dir_path, ignore_dangling_symlinks=True)
        print(f"{dir_name} successfully backed up!\n")
    print("Done! Press any key to return to main menu.")
    utilities.getch()
