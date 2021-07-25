import os
import toml
import pathlib

from src.tui_toolbox import error, warning, progress
from src.tools import GlobalConstants as gcst
from src.tools import *

def read_includes(reg):
    return reg[gcst.INCLUDE_TEXT]

def validate_entry(f):
    return os.path.isfile(f) or os.path.isdir(f)

def expand_path(f):
    if len(f) == 0:
        return f
    p = os.path.expandvars(os.path.expanduser(f))
    if p[-1] == "/":
        return p[:-1]
    return p

def add_targets(targets, reg):
    for path in targets:
        if str(path.absolute()) in reg[gcst.INCLUDE_TEXT]:
            warning("Path {} already registered, ignoring ...".format(path))
            continue
        if os.path.isfile(path) or os.path.isdir(path):
            progress("Registered file {}".format(path))
            reg[gcst.INCLUDE_TEXT].append(str(path.absolute()))
        else:
            warning("Path {} is not a file nor a directory, ignoring...".format(path))

##### CLI

def register(args):
    regfile = get_category_registry_fname(args.category[0])
    reg = load_registry(regfile)

    # Purging paths that doesn't exist anymore
    # reg[gcst.INCLUDE_TEXT] = [p for p in reg[gcst.INCLUDE_TEXT] if (os.path.isfile(p) or os.path.isdir(p))]

    if args.edit:
        progress("Editing register for category {}".format(args.category[0]))
        edit_list_in_plaintext(regfile, [gcst.INCLUDE_TEXT], validate_fct=validate_entry, transform_fct=expand_path)
    else:
        add_targets(args.targets, reg)
        write_registry(regfile, reg)

def validate_register(args):
    if not args.category:
        error("Requires a category for action \"{}\"".format(args.subcmd))
    if not args.edit and not args.targets:
        error("Specify a target to register, or use --edit to use external editor")

def generate_register_parser(parser):
    parser.add_argument("--edit", "-e", help="Edit the list using an external editor. (One by line)", action="store_true")
    parser.add_argument("targets", help="File / Directory to register for backup", type=pathlib.Path, nargs="*")
    #TODO
    #       Register from list in file
    #       Register from user input in file with auto method detection
