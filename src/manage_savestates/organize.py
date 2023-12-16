"""Organize gz files inside of a directory"""
import os
from dataclasses import dataclass
from datetime import date, datetime
import utilities
from utilities import Directory


@dataclass
class GZFile:
    """Stores data about a savestate or macro."""
    prefix: str
    text_of_name: str
    extension: str
    original_name: str


def organize():
    """Get list of savestates and macros and pass it to reorder_files()
    or trim_files().
    """
    header = utilities.box("Manage savestates | Organize files")
    utilities.clear()
    print(f"{header}\n")

    dirs = utilities.load_pickle("dirs.txt")
    if dirs == []:
        utilities.no_dirs_edge_case_handling()
        dirs = utilities.load_pickle("dirs.txt")
        if dirs == []:
            return
    for directory in dirs:
        if not os.path.exists(directory.path):
            print(f"{directory.path} could not be found. Please verify path in settings.")
        elif directory.action is not None:
            log_path = f"{directory.path}/log.txt"
            raw_gz_files = sorted([x for x in os.listdir(directory.path)
                                   if (x.endswith(".gzs") or x.endswith(".gzm"))
                                   and not x.startswith(".")])
            states, macros = [], []
            if not os.path.exists(f"{directory.path}/_other"):
                os.mkdir(f"{directory.path}/_other")
            current_date_and_time = (f"{date.today().strftime('%B %d, %Y')} at"
                                     f" {datetime.now().strftime('%H:%M:%S')}")
            write_to_log(f"{current_date_and_time}\n\n", log_path)

            for file in raw_gz_files:
                packaged_file = package(file)
                if (len(packaged_file.prefix) == 4
                    and len(packaged_file.text_of_name) == 0):
                    os.remove(f"{directory.path}/{packaged_file.original_name}")
                else:
                    if packaged_file.extension == ".gzs":
                        states += [packaged_file]
                    else:
                        macros += [packaged_file]

            if directory.action == "reorder":
                reorder_files(directory.path, states, macros)
            elif directory.action == "trim":
                trim_files(directory.path, states + macros)

            truncate_log(log_path, 2000000)

    print("Done! Press any key to exit.")
    utilities.getch()


def package(file):
    """Returns prefix, text of name, file extension, and complete
    original name of a GZ file as a GZFile object.
    """
    original_name = file
    extension = file[-4:] # last 4 chars
    if file[:3].isdigit() and file[3:4] == "-":
        prefix = file[:4] # first 4 chars
        text_of_name = file[4:-4] # all but first and last 4 chars
    else:
        prefix = ""
        text_of_name = file[:-4] # all but last 4 chars
    packaged_file = GZFile(prefix, text_of_name, extension, original_name)
    return packaged_file


def reorder_files(directory, states, macros):
    """Numbers savestates in the order they are found in the directory,
    renumbers macros to match savestates of the same name, and moves
    all other macros to _other.
    """
    prefix = "-1"
    for state in states:
        prefix = iterate_prefix(prefix)  # essentially returns prefix += 1
        state.prefix = prefix
        rename_file(directory, state, states)
    for macro in macros:
        for state in states:
            if macro.text_of_name == state.text_of_name:
                macro.prefix = state.prefix
                rename_file(directory, macro, macros)
                break
        else:
            move_to_other(directory, macro)
    for state in states:
        for macro in macros:
            if state.text_of_name == macro.text_of_name:
                break
        else:
            with open(f"{directory}/{state.prefix}.gzm", "a",
                      encoding="utf-8"):
                pass


def iterate_prefix(old_prefix):
    """Add 1 to the old prefix number and return a complete prefix,
    i.e. "xxx-".
    """
    # int() strips leading 0s, and str() returns a string.
    state_number = str(int(old_prefix[:3]) + 1)
    new_prefix = f"{'0' * (3 - len(state_number))}{state_number}-"
    return new_prefix


def rename_file(directory, file, files):
    """Rename a given file from list 'files'. File is inside of 
    the variable 'directory'. Renames file from original name to the name 
    passed as var "file".
    """
    file_new_name = f"{file.prefix}{file.text_of_name}{file.extension}"
    log_path = f"{directory}/log.txt"
    if file_new_name != file.original_name:
        if not os.path.exists(f"{directory}/{file_new_name}"):
            os.rename(f"{directory}/{file.original_name}", f"{directory}/"
                      f"{file_new_name}")
            log_message = f"Renamed {file.original_name} to {file_new_name}\n"
            write_to_log(log_message, log_path)
            print(log_message.strip("\n"))
        else:
            list_index = 0
            for other_file in files:
                if other_file.original_name == file_new_name:  # the culprit
                    # delete it from list because we take care of it below
                    del files[list_index]
                    break
                list_index += 1
            suffix = 2
            while os.path.exists(f"{directory}/_other/{file.text_of_name}-"
                                 f"{str(suffix)}{file.extension}"):
                suffix += 1
            os.rename(f"{directory}/{file_new_name}", f"{directory}/_other/"
                      f"{file.text_of_name}-{str(suffix)}{file.extension}")
            log_message = (f"Renamed {file_new_name} to {file.text_of_name}-"
                           f"{str(suffix)}{file.extension} and moved it to"
                           " _other\n")
            write_to_log(log_message, log_path)
            print(log_message.strip("\n"))

            os.rename(f"{directory}/{file.original_name}", f"{directory}/"
                      f"{file_new_name}")
            log_message = f"Renamed {file.original_name} to {file_new_name}\n"
            write_to_log(log_message, log_path)
            print(log_message.strip("\n"))


def move_to_other(directory, file):
    """Moves a file in directory to directory's "_other" directory. Renames
    duplicate file(s) in _other if they exist.
    """
    file_new_name = f"{file.text_of_name}{file.extension}"
    log_path = f"{directory}/log.txt"
    if not os.path.exists(f"{directory}/_other/{file_new_name}"):
        os.rename(f"{directory}/{file.original_name}", 
                  f"{directory}/_other/"f"{file_new_name}")
        if file.original_name == file_new_name:
            log_message = f"Moved {file_new_name} to _other"
        else:
            log_message = (f"Renamed {file.original_name} to {file_new_name}"
                           " and moved it to _other\n")
        write_to_log(log_message, log_path)
        print(log_message.strip("\n"))
    else:
        suffix = 2
        while os.path.exists(f"{directory}/_other/"
                             f"{file.text_of_name}-{str(suffix)}"
                             f"{file.extension}"):
            suffix += 1
        os.rename(f"{directory}/_other/{file_new_name}",
                  f"{directory}/_other/{file.text_of_name}-"
                  f"{str(suffix)}{file.extension}")
        log_message = (f"Renamed {file_new_name} (in _other) to"
                       f" {file.text_of_name}-{str(suffix)}{file.extension}\n")
        write_to_log(log_message, log_path)
        print(log_message.strip("\n"))

        os.rename(f"{directory}/{file.original_name}", f"{directory}/_other/"
                  f"{file_new_name}")
        if file.original_name == file_new_name:
            log_message = f"Moved {file_new_name} to _other"
        else:
            log_message = (f"Renamed {file.original_name} to {file_new_name}"
                           " and moved it to _other\n")
        write_to_log(log_message, log_path)
        print(log_message.strip("\n"))


def trim_files(directory, files):
    """Removes numbered prefixes from all files."""
    for file in files:
        file.prefix = ""
        rename_file(directory, file, files)


def truncate_log(log_path, byte_limit):
    """Truncate file at log_path by cutting off beginning if log is
    larger than byte_limit bytes.
    """
    current_file_length = os.stat(log_path).st_size
    if current_file_length > byte_limit:
        new_start = current_file_length - byte_limit
        with open(log_path, "rb") as old_file:
            with open("/tmp/tmp.txt", "wb") as new_file:
                new_file.write(old_file.read()[new_start:])
            new_file.close()
        old_file.close()
        os.rename("/tmp/tmp.txt", log_path)


def write_to_log(txt, log_path):
    """Writes text to the file at log_path."""
    with open(log_path, "a", encoding="utf-8") as file:
        file.write(txt)
    file.close()
