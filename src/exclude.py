import os

from src.tools import GlobalConstants as gcst
from src.tools import check_exist_else_create, setup_default_registry, write_registry, load_registry, edit_list_in_plaintext
from src.tui_toolbox import error, progress, warning

def read_excludes(reg, excl):
    if excl not in reg[gcst.EXCLUDE_TEXT].keys():
        return []
    else:
        return reg[gcst.EXCLUDE_TEXT][excl]

def read_all_excludes(reg):
    return reg[gcst.EXCLUDE_TEXT]

def generate_excludes(excl):
    for key in ["dirs", "files", "substr"]:
        if key not in excl.keys():
            excl[key] = []
    exclude_dirs = ["--exclude=\"{}/**\"".format(d) for d in excl["dirs"]]
    exclude_files= ["--exclude=\"{}\"".format(f) for f in excl["files"]]
    exclude_substr=["--exclude=\"*{}*\"".format(s) for s in excl["substr"]]
    return " ".join([" ".join(e) for e in [exclude_dirs, exclude_files, exclude_substr]])

def add_excludes(rules, excl_type, reg):
    for rule in rules:
        if rule in reg[gcst.EXCLUDE_TEXT][excl_type]:
            warning("Rule {} already excluded, ignoring ...".format(rule))
            continue
        progress("Excluding {} {}".format(excl_type, rule), heading="{} exclusion".format(excl_type))
        reg[gcst.EXCLUDE_TEXT][excl_type].append(rule)

def exclude(args):
    rootdir = os.path.join(gcst.BACKUP_DIR, args.category[0])
    check_exist_else_create(rootdir)
    
    regfile = os.path.join(rootdir, gcst.REGISTER_FNAME)
    if not os.path.isfile(regfile):
        setup_default_registry(regfile)

    reg = load_registry(regfile)

    if args.edit:
        progress("Editing excludes of type \"{}\" for category {}".format(args.exclude_type, args.category[0]))
        edit_list_in_plaintext(regfile, [gcst.EXCLUDE_TEXT, args.exclude_type])
    else:
        add_excludes(args.excludes, args.exclude_type, reg)
        write_registry(regfile, reg)

def generate_exclude_parser(parser):
    parser.add_argument('exclude_type', choices=gcst.EXCLUDES_TYPES, help='The type of exclusion you want')
    parser.add_argument("--edit", "-e", help="Edit the list using an external editor. (One by line)", action="store_true")
    parser.add_argument("excludes", help="The rules to add to exclusion list", nargs="*")

def validate_exclude(args):
    if not args.exclude_type:
        error("Need to specify what type of exclusion will you use")
    if not args.category:
        error("Requires a category for action \"{}\"".format(args.subcmd))
    if not args.edit and not args.excludes:
        error("Specify a rule to exclude, or use --edit to use external editor")
