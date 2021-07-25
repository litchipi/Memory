# Memory
Backup tool easy to use in CLI

## Work in progress, do not use yet.

## Requierements

`sudo apt install tar gpg xz-utils python3`

`pip install toml argcomplete argparse`

## How to install ?
./install.sh
Will create a folder `~/.local/share/memory/` and copy the code inside, then create a symlink to `~/.local/bin/memory`

## How it works ?
Memory creates a `register.toml` file in a specific directory for each backup category. In it, it stores what to include, what to exclude and the last backup time.
When asking to backup, the script reads the register, and format the parameters to be passed the the `tar` command (for archiving / compression) or the `gpg` command (for encryption).
The files are first putted as symlinks inside a tmp directory, so the file archive doesn't have the full path.

The final archive looks like:
```
category.tar
| enc.tar.gpg
| cmp.tar.xz
| stored.tar
| enc_cmp.tar.xz.gpg
```

The registers and final archives are located in `~/.backup/`

## How to use it ?

#### Backup the category "test"
`memory backup test`

(pass `-f` to force backup even if not file changed)

#### Backup all categories
`memory all`

(pass `-f` to force backup even if not file changed)

#### Add a new file / dir to a backup "test"

`memory register test c file.txt`
Will register file `file.txt` for a backup in category `test` with backup method `c`

`memory register test ce dir/`
Will register directory `dir/` for a backup in category `test` with backup method `ce`

Options are:
- s: Stored (no compression, no encryption)
- c: Compressed (compression, no encryption) DEFAULT
- e: Encrypted (no compression, encryption)
- ce: Compressed + Encrypted

#### Edit the files registered in an editor
Use the option `--edit`:

`memory register test ce --edit`

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
By default, you get some metadata about the categories as well, use option `-n`
