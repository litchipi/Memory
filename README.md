# Memory
Backup tool easy to use in CLI

## Work in progress, do not use yet.

## Requierements

`sudo apt install tar gpg xz-utils python3`
`pip install toml`



# OLD README

## How to install ?
./install.sh

Will copy the files under a .local directory
Will create some aliases to ease the usage

## How to use it ?

### Register a file
`bck_register -c my_images -m ce Me_and_my_girlfriend.jpg other_images/`

Registers the image and the folder passed as argument for backup in the "my_images" category.
ce: Will backup using compression + encryption on those files.
Note: All the files inside the folder will be added for backup using the same options

### Create exclusion rules
`bck_exclude -c dev_bck dirs __pycache__`

Will not include any `__pycache__` folder found inside the backup of the category `dev_bck`

`bck_exclude file_ext .pyc`

Will not include any file having the extension `.pyc`.
Will add this rule for every categories, and will automatically add it to new ones

`bck_exclude file_contains not_this`

Will not include any file in which the substring "not_this" can be found
Will add this rule for every categories, and will automatically add it to new ones

### Backup
`backup -c my_images`

Starts the process of creating the backup for the category 'my_images'.
Will output a `my_images.tar` inside the folder `~/.backup/`, itself containing a `cmp.tar.xz` for compressed data, `enc.tar.gpg` for encrypted data, `cmp_enc.tar.xz.gpg` for encrypted + compressed data, `stored.tar` for stored only data.
