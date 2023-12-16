# manage-savestates

## Overview

Organizes and labels files. Designed to be used with savestates and macros generated using [gz](https://github.com/glankk/gz), also known as "the practice ROM" for The Legend of Zelda: Ocarina of Time speedrunning.

Should also work with files made using [kz](https://github.com/krimtonz/kz) (The Legend of Zelda: Majora's Mask practice ROM) but this is untested.

## Usage

After installation, run 

`mansav` 

in the command line and the program's menu will appear. Press 1, 2, 3, or 4 to choose an option.

These are the options:

### 1. Organize directories

Any directories containing savestates and macros you want to organize will be organized. Any changes made to any file will be printed to the console and a log (stored in the directory).

Every time you use the program, the directories you organize will be saved, so you won't have to re-select them every time. If you've never used the program before, selecting this option prompts you to choose one or more directories to organize and your preferred organization method. Since each directory has its own organization method, you can choose the setting that works best for a given route, etc. without compromising your other files. You can add or remove directories in settings later. (See the Settings explanation for more details on organization methods.)

### 2. Back up directories

Easily back up your savestates and macros to a destination of your choice. The first time you use the program, it will prompt you to choose a directory. You can change this later in settings.

### 3. Settings

The settings menu also has three options: add/delete directory (from the list of directories you organize/ back up, NOT from your hard drive), change organization method/ path for a directory, and change the directory for storing backups. I believe the first and third options are fairly straightforward; here's the explanation for organization methods. Note that organization methods are not set globally, but on a directory-by-directory basis, so settings can differ between different directories with different purposes.

#### Trim numbered prefixes from files

When applied to a directory, this option removes the default prefix attached to savestates by gz (e.g., 000-savestate-name.gzs would become savestate-name.gzs). If you prefer to have your savestates in alphabetical order or just don't like the numbers, this setting is for you. Note that this cannot easily be undone if you have a large amount of savestates, so be careful!

#### Renumber savestates and macros based on their names

The practice ROM assigns numbers to savestates automatically, but if you are the kind of person that likes to renumber them manually so they are in order (especially if you find yourself wanting to make new savestates at the beginning of a route but don't want to rename dozens or hundreds of files), you will probably find this setting useful. This setting renumbers the states in order from 000 to 999 in the order they are found in your folder. If you have 150 savestates in a folder and you want to add a new savestate between 002 and 003, you could name it something like "002-z[savestate name]", then run this program; it and all the states after it will then be numbered correctly. 

The second major feature of this setting is that if there is a macro that has the same name as a savestate, the macro will be numbered so it matches the corresponding savestate. For example, if you have a savestate called "021-dot skip.gzs" and a macro called "dot skip.gzm", the macro will be renamed "021-dot skip.gzm". The macro's number will be adjusted to the correct one if the savestate's number changes. 

For quality of life purposes, for each savestate that doesn't have a corresponding macro, a dummy macro will be made. If you have no macro matching "042-wasteland hess.gzs", a dummy file "042-.gzm" will be created. This makes it so that when you go to import macros in gz, the cursor will be at the same place in both savestate and macro lists--so no more scrolling forever to find the macro that matches the savestate you just loaded in. It also de facto fixes the bug that occurs when you have more savestates than macros that forces you to reload the SD card.

Finally, any macro in the directory that does NOT have a matching savestate is moved to a subdirectory called "_other" (it will be at the top in gz). In addition, if you already have a macro (e.g., "120-collapse skip.gzm") and you make a new one with the same name (e.g., "collapse skip.gzm"), when the program attempts to rename the new macro, it will label the old macro with a numbered suffix and place it in "_other", and the new one will be numbered in its place. So in this example, 120-collapse skip.gzm would be renamed collapse skip-2.gzm and placed in _other, and collapse skip.gzm would be renamed 120-collapse skip.gzm. So if you find a new strat to replace an old one and want to make a macro of it, for example, just make it, and the old one will be filed away automatically in case you want to reference it again later.

### 4. Quit

Exit the program!

## Installation

The easiest way to install this program is using pip.

### Windows

In the console, type `py -m pip install manage-savestates`

### macOS

In the console, type `python3 -m pip install manage-savestates`

### Linux

This program is untested on Linux but I believe it should work.

Alternatively, on any platform, download the source code, navigate to /manage-savestates/src/manage_savestates in the console, and run 

`python3 manage_savestates.py`