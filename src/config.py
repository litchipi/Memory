import os
import toml
import subprocess

from src.tools import GlobalConstants as gcst

from src.tui_toolbox import error, progress, warning
from src.tools import edit_list_in_plaintext

def get_config_fname(cat):
    return os.path.join(gcst.BACKUP_DIR, cat, "config.toml")

def create_config_if_not_exist(cat):
    if not os.path.isfile(get_config_fname(cat)):
        setup_default_config(cat)

def setup_default_config(cat):
    with open(get_config_fname(cat), "w") as f:
        toml.dump(gcst.DEFAULT_CAT_CONFIG, f)

def loop_edit_config(fname):
    if len(gcst.DEFAULT_CAT_CONFIG.keys()) == 0:
        warning("No configuration yet supported")
        return
    while True:
        with open(fname, "r") as f:
            print(f.read())
        cfg = input("\nEnter configuration group to edit: [q to exit]\t")
        if cfg.lower() == "q":
            break
        elif cfg not in gcst.DEFAULT_CAT_CONFIG.keys():
            print("No such config group \"{}\", select one of:\n\t{}".format(cfg, ", ".join(gcst.DEFAULT_CAT_CONFIG.keys())))
            continue
        edit_list_in_plaintext(fname, cfg)


#TODO   Implement GlobalConstants modification through "config" cli cmd


##### CLI

def config(args):
    if args.config_cmd == "edit":
        create_config_if_not_exist(args.category[0])
        loop_edit_config(get_config_fname(args.category[0]))

def generate_config_parser(parser):
    sub = parser.add_subparsers(dest="config_cmd", help="Quick config commands")
    edit = sub.add_parser("edit", help="Edit rules")

def validate_config(args):
    if not args.category:
        error("Requires a category for action \"{}\"".format(args.subcmd))
    if len(args.category) > 1:
        error("Cannot perform \"{}\" action on more than 1 category".format(args.subcmd))
    if not args.config_cmd:
        error("Requires a command")
