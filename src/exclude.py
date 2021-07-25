import os
import pathlib

from src.tools import GlobalConstants as gcst
from src.tools import *
from src.tui_toolbox import error, progress, warning

def read_excludes(reg, excl):
    if excl not in reg[gcst.EXCLUDE_TEXT].keys():
        return []
    else:
        return reg[gcst.EXCLUDE_TEXT][excl]

def read_all_excludes(reg):
    return reg[gcst.EXCLUDE_TEXT]

def generate_excludes(excl):
    for key in gcst.EXCLUDES_TYPES:
        if key not in excl.keys():
            excl[key] = []
    
    excludes = list()
    for excl_rule in excl.keys():
        if excl_rule == "dirs":
            excludes.extend(["--exclude=\"{}/**\"".format(d) for d in excl[excl_rule]])
        elif excl_rule == "substr":
            excludes.extend(["--exclude=\"*{}*\"".format(s) for s in excl[excl_rule]])
        else:
            excludes.extend(["--exclude=\"{}\"".format(f) for f in excl[excl_rule]])
    return " ".join(excludes)

def add_excludes(rules, excl_type, reg):
    for rule in rules:
        if excl_type not in reg[gcst.EXCLUDE_TEXT]:
            reg[gcst.EXCLUDE_TEXT][excl_type] = list()
        if rule in reg[gcst.EXCLUDE_TEXT][excl_type]:
            warning("Rule {} already excluded, ignoring ...".format(rule))
            continue
        progress("Excluding {} {}".format(excl_type, rule), heading="{} exclusion".format(excl_type))
        if excl_type == "path":
            rule = str(pathlib.Path(rule).absolute())
        reg[gcst.EXCLUDE_TEXT][excl_type].append(rule)

def exclude(args):
    regfile = get_category_registry_fname(args.category[0])
    reg = load_registry(regfile)

    if args.edit:
        progress("Editing excludes of type \"{}\" for category {}".format(args.exclude_type, args.category[0]))
        edit_list_in_plaintext(regfile, [gcst.EXCLUDE_TEXT, args.exclude_type])
    else:
        add_excludes(args.excludes, args.exclude_type, reg)
        export_to_file(regfile, reg)

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
