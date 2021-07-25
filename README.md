# Memory
Backup tool easy to use in CLI

## Work in progress, do not use yet.

## Requierements

`sudo apt install restic`

`pip install argcomplete argparse`

## How to install ?
./install.sh
Will create a folder `~/.local/share/memory/` and copy the code inside, then create a symlink to `~/.local/bin/memory`

## How it works ?
Memory creates a `register.json` file in a specific directory for each backup category. In it, it stores what to include, andwhat to exclude.
When asking to backup, the script reads the register, and format the parameters to be passed the the `restic` command (backup & archiving tool).

The registers and resulting restic repositories are located in `~/.backup/`
Please check the `restic` documentation for usage of repositories.

## How to use it ?

#### Backup the category "test"
`memory backup test`

(pass `-f` to force backup even if not file changed)

#### Backup all categories
`memory all`

(pass `-f` to force backup even if not file changed)

#### Add a new file / dir to a backup "test"
`memory register test file.txt`
Will register file `file.txt` for a backup in category `test`

#### Edit the files registered in an editor
Use the option `--edit`:

`memory register test --edit`

Will open an editor (vim by default), with 1 registered file / dir per line.
Please use absolute path when adding more, or only use to delete some

#### Exclude some files from being backed up
To remove all files with the `.pyc` extension:

`memory exclude test files '*.pyc'`
*Note: The ' is mandatory to avoid bash replacing the wildcard with names*

#### Exclude some dirs from being backup up
To remote all `.git` dirs:

`memory exclude test dirs .git`

#### Edit the exclusions rules in an editor
Use the option `--edit`

`memory exclude test files --edit`

Edit the `files` exclusion rules in an external editor

#### Edit the register in a text editor
`memory edit test`

#### Check if backups has to be done again
`memory check test`

#### List all categories
`memory ls`
By default, you get some metadata about the categories as well, use option `-n` if you want only the
raw list of categories

#### Inspect a directory in registries
`memory inspect ~`
Will check if the given path is registered inside one or more categories.
You can pass options `-i` to get more info (such as the latest snapshot taken), and the `-l` option
to inspect every file and directory inside the path given (will perform normal inspect if path is a
file)
