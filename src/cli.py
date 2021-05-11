import sys
import pathlib
import argparse

from src.tools import GlobalConstants as gcst
from src.tui_toolbox import error, warning, progress
from src.backup import validate_backup, generate_backup_parser, backup, validate_backup_all, generate_backup_all_parser, backup_all
from src.register import validate_register, generate_register_parser, register
from src.config import validate_config, generate_config_parser, config
from src.exclude import validate_exclude, generate_exclude_parser, exclude

SUBCMD_FCTS = {
        "backup": [generate_backup_parser, validate_backup, backup, "Backup one or more categories"],
        "all": [generate_backup_all_parser, validate_backup_all, backup_all, "Backup all categories"],
        "register": [generate_register_parser, validate_register, register, "Register new files / folders for backup"],
        "exclude": [generate_exclude_parser, validate_exclude, exclude, "Exclude files / folders for backup"],
        "config": [generate_config_parser, validate_config, config, "Configure backup tool"],
        }


def generate_parser():
    parser = argparse.ArgumentParser()
    
    subparsers = parser.add_subparsers(dest="subcmd", help='Commands to manage backups')

    SUBCMD_FCTS[gcst.DEFAULT_SUBCMD][0](parser)
    for key, data in SUBCMD_FCTS.items():
        if key == gcst.DEFAULT_SUBCMD: continue
        data[0](subparsers.add_parser(key, help=data[3]))
    
    return parser

def validate_args(args, parser):
    if (not args.subcmd) and (not args.category):
        parser.print_help()
        sys.exit(0)

    if not args.subcmd:
        SUBCMD_FCTS[gcst.DEFAULT_SUBCMD][1](args)
    elif args.subcmd in SUBCMD_FCTS.keys():
        SUBCMD_FCTS[args.subcmd][1](args)
    else:
        error("Subcommand {} not recognized".format(args.subcmd))

def parse_args():
    parser = generate_parser()
    args = parser.parse_args()
    validate_args(args, parser)
    return args

def get_commands_handlers():
    handlers = {key:fct[2] for key, fct in SUBCMD_FCTS.items() if key != gcst.DEFAULT_SUBCMD}
    handlers["__default__"] = SUBCMD_FCTS[gcst.DEFAULT_SUBCMD][2]
    return handlers
