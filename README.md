# About

Organizes and labels files. Designed to be used with savestates and macros generated using [gz, a.k.a. "The Practice ROM"](https://github.com/glankk/gz), a practice tool for Ocarina of Time speedrunning.

# Usage

After [installation](#installation), run `$ mansav` to open the GUI interface.

A command line interface will be added in the future.

## Features

### Organize directories

Organize directories of gz savestates and / or macros according to your specifications. The program remembers which directories you want organized and the settings associated with each directory.

#### Available settings

##### Trim

Trims the default numbered prefix gz attaches to savestates (e.g., 000-savestate-name.gzs -> savestate-name.gzs). Good if you keep your savestates in alphabetical order.

##### Renumber

Renumbers savestates from 000 up to 999 in the order they are displayed in gz's file system. Good if you like to renumber savestates manually so they are in route order, especially if you want to insert savestates at the beginning of a route but don't want to rename dozens or hundreds of other files. This setting renumbers the states in order from 000 to 999 in the order they are found in your folder. If you have 150 savestates in a folder and you want to add a new savestate between 002 and 003, you could name it something like "002-z[savestate name]", then run this program; it and all the states after it will then be numbered correctly. 

Additionally, macros that have the same name as a savestate are numbered to match their corresponding savestates. For example, if you have a savestate called "021-dot skip.gzs" and a macro called "dot skip.gzm", the macro will be renamed "021-dot skip.gzm". Duplicate macros and macros with no matching savestate are moved to a subfolder called "_other" to keep folders organized (the underscore puts it at the top of the file explorer in gz).

For quality-of-life purposes, the program creates an empty macro for each savestate that doesn't have a corresponding macro (e.g., for a state "042-wasteland hess.gzs" with no matching macro, the empty macro "042-.gzm" is generated). This means that when loading macros in gz, the cursor will always at the same place in savestate and macro lists, avoiding the bug that forces you to reload the SD card.

##### Do nothing

Good if you want to back up a certain folder with the rest, but don't want the program to touch it otherwise.

### Back up directories

Copy the directories you chose to a backup destination.

# Installation

This program requires Python >= 3.7.

### Windows and macOS

#### Option 1: pip

The easiest way to install this program is using pip: `$ pip install manage-savestates`

#### Option 2: download and run

Download the source code and run main.py: `$ python3 /path/to/main.py`

### Linux

This program has not been tested on Linux.
