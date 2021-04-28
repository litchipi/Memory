import os
import toml
import pathlib

from src.tui_toolbox import error, warning, progress
from src.tools import GlobalConstants as gcst
from src.tools import check_exist_else_create, edit_list_in_plaintext

def setup_default_register(fname):
    with open(fname, "w") as f:
        toml.dump(gcst.DEFAULT_CAT_REGISTER, f)

def write_register(fname, reg):
    with open(fname, "w") as f:
        toml.dump(reg, f)

def load_register(fname):
    with open(fname, "r") as f:
        reg = toml.load(f)
    __validate_register(reg)
    return reg

def __validate_register(reg):
    if "include" not in reg.keys() or "exclude" not in reg.keys():
        error("Register file corrupted")



def read_includes(reg, mode):
    if mode not in gcst.BACKUP_METHODS:
        error("Mode {} does not exist".format(mode))
    return reg["include"][mode]

def validate_entry(f):
    return os.path.isfile(f) or os.path.isdir(f)

def expand_path(f):
    if len(f) == 0:
        return f
    p = os.path.expandvars(os.path.expanduser(f))
    if p[-1] == "/":
        return p[:-1]
    return p

def add_targets(targets, method, reg):
    for path in targets:
        if path in reg["include"][method]:
            warning("Path {} already registered, ignoring ...".format(path))
            continue
        if os.path.isfile(path) or os.path.isdir(path):
            progress("Registered file {}".format(path))
            reg["include"][method].append(str(path.absolute()))
        else:
            warning("Path {} is not a file nor a directory, ignoring...".format(path))

##### CLI

def register(args):
    rootdir = os.path.join(gcst.BACKUP_DIR, args.category[0])
    check_exist_else_create(rootdir)

    regfile = os.path.join(rootdir, gcst.REGISTER_FNAME)
    if not os.path.isfile(regfile):
        setup_default_register(regfile)

    reg = load_register(regfile)

    # Purging paths that doesn't exist anymore
    reg["include"] = {m:[p for p in l if (os.path.isfile(p) or os.path.isdir(p))] for m, l in reg["include"].items()}

    if args.edit:
        progress("Edit")
        edit_list_in_plaintext(regfile, ["include", args.method], validate_fct=validate_entry, transform_fct=expand_path)
    else:
        add_targets(args.targets, args.method, reg)
        write_register(regfile, reg)

def validate_register(args):
    if not args.method:
        error("Need to specify what method to use to backup")
    if not args.category:
        error("Requires a category for action \"{}\"".format(args.subcmd))
    if len(args.category) > 1:
        error("Cannot perform \"{}\" action on more than 1 category".format(args.subcmd))
    if not args.edit and not args.targets:
        error("Specify a target to register, or use --edit to use external editor")

    if args.edit and args.method == "a":
        args.method = "c"

def generate_register_parser(parser):
    parser.add_argument("--method", "-m", help="Method to use to backup (a: auto (w/ file extension, method \"c\" if unknown), ce: compressed + encrypted, c: compressed, e: encrypted, s: stored).",
            choices=gcst.BACKUP_METHODS + ["a"], default='a')
    parser.add_argument('--category', '-c', action='append', help='The name of the category you want to backup')
    parser.add_argument("--edit", "-e", help="Edit the list using an external editor. (One by line)", action="store_true")
    parser.add_argument("targets", help="File / Directory to register for backup", type=pathlib.Path, nargs="*")
    #TODO
    #       Register from list in file
    #       Register from user input in file with auto method detection
