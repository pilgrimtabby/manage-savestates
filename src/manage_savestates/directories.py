"""Organize and back up gz macros and savestates in a directory.

Classes:
    GZFile(prefix: str, text_of_name: str, extension: str,
        original_name: str)

Functions:
    organize()
    convert_to_gzfile(filename: str)
    trim_files(path: str, states: list, macros: list)
    renumber_files(path: str, states: list, macros: list)
    iterate_prefix(prefix: str | int | float)
    rename_file(orig_path: str, dest_path: str, file: GZFile,
        file_list: list)
    delete_from_file_list(file: GZFile, file_list: list)
    get_unique_name(path: str, file: GZFile)
    write_to_log(txt: str, log_path: str)
    remove_empty_log_entry(log_path: str, timestamp: str)
    remove_newline_at_top(log_path: str)
    truncate_from_beginning(file_path: str, byte_limit: int)
    back_up()
"""
import os
import shutil
import time
from dataclasses import dataclass
from datetime import date, datetime
import common
import settings


@dataclass
class GZFile:
    """Store information about a gz savestate or macro file.
    
    Attributes:
        prefix (str): Either three numbers and a dash (xxx-) if
            that's how the file name starts (the default gz
            configuration for savestate files), or an empty string.
        text_of_name (str): The entire file name except for prefix
            and extension.
        extension (str): The file extension.
            .gzs: File extension for savesetate files.
            .gzm: File extension for macro files.
        original_name: The full name of the file when a GZFile object
            is instantiated, including its extension.
    """
    prefix: str
    text_of_name: str
    extension: str
    original_name: str


def organize():
    """Organize files inside of each GZDirectory.
    
    For each GZDirectory object, create lists of savestate and macro
    files (excluding "dummy" macro files, which are deleted), and pass
    them into trim_files() or renumber_files() if GZDirectory.action is
    not None.
    """
    header = common.box("Manage savestates | Organize files")
    dirs = common.load_pickle("gzdirs.txt")

    # Prompt user to add directories if none have been added yet
    if dirs == []:
        common.clear()
        print(f"{header}\n\nNo directories have been added yet!\nGoing to settings...")
        time.sleep(2)
        settings.add_gzdir()
        dirs = common.load_pickle("gzdirs.txt")
        if dirs == []:
            return
    common.clear()
    print(f"{header}\n")

    for gzdirectory in dirs:
        if not os.path.exists(gzdirectory.path):
            print(f"{gzdirectory.path} could not be found. Skipping...")

        elif gzdirectory.action is not None:
            print(f"Organizing files in {gzdirectory.path}")

            # Create list of savestate and macro files in GZDirectory
            state_and_macro_names = sorted([x for x in os.listdir(gzdirectory.path)
                                           if (x.endswith(".gzs") or x.endswith(".gzm"))
                                           and not x.startswith(".")])  # Exclude hidden files

            states, macros = [], []
            for filename in state_and_macro_names:
                gzfile = convert_to_gzfile(filename)
                if gzfile.extension == ".gzs":
                    states += [gzfile]
                else:
                    # Delete dummy macro files (see renumber_files() and
                    # README.md for more information)
                    if gzfile.prefix != "" and gzfile.text_of_name == "":
                        os.remove(f"{gzdirectory.path}/{gzfile.original_name}")
                    else:
                        macros += [gzfile]

            # Make initial log entry
            log_path = f"{gzdirectory.path}/log.txt"
            timestamp = (f"{date.today().strftime('%B %d, %Y')} at "
                         f"{datetime.now().strftime('%H:%M:%S')}")
            write_to_log(f"\n{timestamp}\n", log_path)

            if gzdirectory.action == "trim":
                trim_files(gzdirectory.path, states, macros)
            elif gzdirectory.action == "renumber":
                renumber_files(gzdirectory.path, states, macros)

            # Clean up log
            remove_empty_log_entry(log_path, timestamp)
            truncate_from_beginning(log_path, 2000000)
            remove_newline_at_top(log_path)

    input("Done! Press enter to exit: ")


def convert_to_gzfile(filename):
    """Returns a GZFile object from a filename.
    
    Args:
        filename (str): The full name of a file, including extension
            (but not its path).
    
    Returns:
        GZFile object: See GZFile class documentation.
    """
    original_name = filename
    extension = filename[-4:]  # The last 4 characters
    # Prefix is first 4 characters if they are three digits and a dash
    if filename[:3].isdigit() and filename[3:4] == "-":
        prefix = filename[:4]
        text_of_name = filename[4:-4]  # Name excluding prefix, extens.
    else:
        prefix = ""
        text_of_name = filename[:-4]  # No prefix, exclude extension
    return GZFile(prefix, text_of_name, extension, original_name)


def trim_files(path, states, macros):
    """Remove numbered prefixes from all files.
    
    Args:
        path (str): Absolute path to directory holding the files.
        states (list): List of GZFiles that are savestates.
        macros (list): List of GZFiles that are macros.
    """
    files = states + macros
    for file in files:
        if file.prefix != "":
            file.prefix = ""
            rename_file(path, path, file, files)


def renumber_files(path, states, macros):
    """Renumber savestate files in the order they are listed on Windows
    and macOS, renumber macros to match savestates with matching
    text_of_name if matching savestates exist, move all other
    macros to path/_other, then create blank "dummy" macros for
    savestates with no matching macro. (For the reason why, see
    README.md.)

    Args:
        path (str): Path to the directory holding the files.
        states (list): List of savestate (.gzs) files passed in from
            organize().
        macros (list): List of macro (.gzm) files passed in from
            organize().
    """
    # Renumber savestates in order
    prefix = "000"
    for state in states:
        if state.prefix != f"{prefix}-":
            state.prefix = f"{prefix}-"
            rename_file(path, path, state, states)

        # Renumber macro with matching text_of_name if it exists
        matching_macros = 0
        for macro in macros:
            if macro.text_of_name == state.text_of_name:
                matching_macros += 1
                if macro.prefix != state.prefix:
                    macro.prefix = state.prefix
                    rename_file(path, path, macro, macros)

        # Create dummy macro if no matching macro exists
        if matching_macros == 0:
            with open(f"{path}/{state.prefix}.gzm", "a", encoding="utf-8"):
                pass

        prefix = iterate_prefix(prefix)

    # After renumbering, move macros with no match to _other
    for macro in macros:
        if macro.prefix == "":
            rename_file(path, f"{path}/_other", macro, None)
            continue
        for state in states:
            if macro.text_of_name == state.text_of_name:
                break
        else:
            rename_file(path, f"{path}/_other", macro, None)


def iterate_prefix(prefix):
    """Iterate a number and return it as a string of at least 3 digits.

    Args:
        prefix (str | int | float): A number. Floats are rounded down.
            Strings must not contain decimals.

    Returns:
        new_prefix (str): The iterated number, including leading zeros.
            A string is used to accommodate leading zeros.
    """
    iterated_number = int(prefix) + 1
    leading_zero_count = max(3 - len(str(iterated_number)), 0)
    leading_zeros = "0" * (leading_zero_count)

    return f"{leading_zeros}{iterated_number}"


def rename_file(orig_path, dest_path, file, file_list):
    """Rename file at orig_path from file.original_name to the sum
    of its attributes (prefix, text_of_name, and extension) at
    dest_path.
    
    Before doing so, check if another file with the new name (prefix,
    text_of_name, and extension) exists at dest_path. If so, rename
    that file and move it to _other if it's not already there.
    
    Args:
        orig_path (str): Path to the file being renamed. orig_path
            is never an _other directory; it is always the .path
            attribute of a GZDirectory.
        dest_path (str): Where the file being renamed is going. Can
            be the .path attribute of a GZDirectory, or the _other dir
            nested inside.
        file (GZFile): The file being renamed.
        file_list (list): The list of which file is an element.
    """
    new_name = f"{file.prefix}{file.text_of_name}{file.extension}"
    log_path = f"{orig_path}/log.txt"

    if not os.path.exists(f"{dest_path}/{new_name}"):
        os.rename(f"{orig_path}/{file.original_name}", f"{dest_path}/{new_name}")

        if file.original_name == new_name:
            log_message = f"Moved {new_name} to _other\n"
        else:
            if dest_path == orig_path:
                log_message = f"Renamed {file.original_name} to {new_name}\n"
            else:
                log_message = (f"Renamed {file.original_name} to {new_name} and moved it to "
                               "_other\n")
        write_to_log(log_message, log_path)
        print(log_message.strip("\n"))

    else:
        delete_from_file_list(file, file_list)
        unique_name = get_unique_name(f"{orig_path}/_other", file)

        os.rename(f"{dest_path}/{new_name}", f"{orig_path}/_other/{unique_name}")
        os.rename(f"{orig_path}/{file.original_name}", f"{dest_path}/{new_name}")

        # Log renaming of file whose name started out as new_name.
        if dest_path != orig_path:
            log_message = f"Renamed {new_name} to {unique_name}\n"
        else:
            log_message = f"Renamed {new_name} to {unique_name} and moved it to _other\n"
        write_to_log(log_message, log_path)
        print(log_message.strip("\n"))

        # Log renaming of original file, which was renamed to new_name.
        if dest_path == f"{orig_path}/_other":
            log_message = f"Renamed {file.original_name} to {new_name} and moved it to _other\n"
        else:
            log_message = f"Renamed {file.original_name} to {new_name}\n"
        write_to_log(log_message, log_path)
        print(log_message.strip("\n"))


def delete_from_file_list(file, file_list):
    """Remove a file from file_list whose original_name is the same as
    the new name of a different file.
    
    This is done so that renumber_files() doesn't try to operate on
    the file after it's been moved to _other.

    Args:
        file (GZFile): The file to be deleted from file_list.
        file_list (list): The list of files.
    """
    if file_list is not None:
        index = 0
        for other_file in file_list:
            if other_file.original_name == f"{file.prefix}{file.text_of_name}{file.extension}":
                del file_list[index]
                break
            index += 1


def get_unique_name(path, file):
    """Return a unique name for a file.
    
    Args:
        path (str): Destination directory for the newly named file.
            This is always an _other directory.
        file (GZFile): The file being renamed.

    Returns:
        str: The unique new name of the file (not a full path).
    """
    suffix = 2
    while os.path.exists(f"{path}/{file.prefix}{file.text_of_name}-{str(suffix)}{file.extension}"):
        suffix += 1
    return f"{file.prefix}{file.text_of_name}-{str(suffix)}{file.extension}"


def write_to_log(txt, log_path):
    """Write text to the file at log_path.
    
    Args:
        txt (str): The text to write.
        log_path (str): Path to the log file.
    """
    with open(log_path, "a", encoding="utf-8") as file:
        file.write(txt)


def remove_empty_log_entry(log_path, timestamp):
    """Remove log entry if the only text written was the timestamp.
    
    Args:
        log_path (str): Path to the log file.
        timestamp (str): Timestamp written to the log.
    """
    with open(log_path, "r", encoding="UTF-8") as log:
        log_contents = log.readlines()
    if log_contents[-1] == f"{timestamp}\n":
        with open(log_path, "w", encoding="UTF-8") as log:
            log_contents[-2] = ""  # Overwriting a newline
            log_contents[-1] = ""  # Overwriting timestamp + newline
            log.writelines(log_contents)


def remove_newline_at_top(log_path):
    """Remove newline at top of the log (happens on first log entry).
    
    Args:
        log_path (str): Path to the log file.
    """
    with open(log_path, "r", encoding="UTF-8") as log:
        log_contents = log.readlines()
    # Avoid error thrown if log_contents[0] doesn't exist
    if len(log_contents) > 0 and log_contents[0] == "\n":
        with open(log_path, "w", encoding="UTF-8") as log:
            log_contents[0] = ""
            log.writelines(log_contents)


def truncate_from_beginning(file_path, byte_limit):
    """Delete data from beginning of file at file_path file's too big.

    Args:
        file_path (str): Path to the file to truncate.
        byte_limit (int): Maximum desired size of the file in bytes.
    """
    current_length = os.stat(file_path).st_size
    if current_length > byte_limit:
        new_start = current_length - byte_limit
        with open(file_path, "r", encoding="UTF-8") as file:
            truncated_content = file.read()[new_start:]
        with open(file_path, "w", encoding="UTF-8") as file:
            file.write(truncated_content)


def back_up():
    """Back up all GZDirectories to a backup directory."""
    header = common.box("Manage savestates | Back up directories")
    gzdirs = common.load_pickle("gzdirs.txt")

    # Return if no GZDirectories yet
    if gzdirs == []:
        common.clear()
        print(f"{header}\n\nNo directories have been added yet!")
        time.sleep(2)
        return

    # Get backup path if not yet chosen
    backups_path = common.load_pickle("backups_path.txt")
    if backups_path == [] or not os.path.exists(backups_path):
        common.clear()
        print(f"{header}\n\nPlease select a directory to store backups:")
        backups_path = common.get_file_path(file_type="dir")
        if backups_path == "":
            return
        common.dump_pickle(backups_path, "backups_path.txt")

    common.clear()
    print(f"{header}\n\nBackups directory is:\n{backups_path}\n\nNow backing up:")

    # Make timestamped directory to house backups, and copy each GZDir
    for directory in gzdirs:
        dir_name = os.path.basename(directory.path)
        if not os.path.isdir(f"{backups_path}/{dir_name}"):
            os.mkdir(f"{backups_path}/{dir_name}")
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        backup_path = f"{backups_path}/{dir_name}/{timestamp}"

        # Account for the fact that sometimes not all files are copied
        print(f"{directory.path}")
        try:
            shutil.copytree(directory.path, backup_path, ignore_dangling_symlinks=True)
        except shutil.Error as error:
            print(f"Some files were not copied:\n{error}")

    input("\nDone! Press enter to return to the main menu: ")
