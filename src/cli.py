import sys
import pathlib
import argparse

from src.tools import GlobalConstants as gcst

from src.tui_toolbox import error, warning, progress
from src import get_subcmd_fcts

SUBCMD_FCTS = get_subcmd_fcts()

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
