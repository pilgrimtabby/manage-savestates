"""Backs up all directories saved in the program to a specified backup directory
   (the directory can be changed in settings)."""
import os
import shutil
import time
import common

def copy_dir():
    """Backs up dir from dir_path to backups_path."""
    dirs = common.load_pickle("dirs.txt")
    # prompts user to select a directory if none are saved
    if dirs == []:
        common.no_dirs_edge_case_handling()
        dirs = common.load_pickle("dirs.txt")
        if dirs == []:
            return  # if no directory selected
    backups_path = common.load_pickle("backups_path.txt")
    header = common.box("Manage savestates | Back up directories")

    # get location for backups if it's not saved or if path doesn't exist
    if backups_path == [] or not os.path.exists(backups_path):
        common.clear()
        print(f"{header}\n\nPlease select a directory to store backups:")
        time.sleep(1)
        backups_path = common.get_dir_path()
        if backups_path == "":
            return  # if no directory selected
        common.dump_pickle(backups_path, "backups_path.txt")  # save new selection

    common.clear()
    print(f"{header}\n")
    # for each directory, back up to its own timestamped folder within the backup directory
    for directory in dirs:
        dir_name = os.path.basename(directory.path)
        # create folder where the timestamped folders are saved for the given directory
        if not os.path.isdir(f"{backups_path}/{dir_name}"):
            os.mkdir(f"{backups_path}/{dir_name}")

        current_datetime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        backed_up_dir_path = f"{backups_path}/{dir_name}/{current_datetime}"
        header = common.box("Manage savestates | Back up directories")
        print(f"Now copying\n{directory.path} to\n{backed_up_dir_path}")
        shutil.copytree(directory.path, backed_up_dir_path, ignore_dangling_symlinks=True)
        print(f"{dir_name} successfully backed up!\n")
    print("Done! Press any key to return to main menu.")
    common.getch()
