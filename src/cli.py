import sys
import pathlib
import argparse

from src.tools import GlobalConstants as gcst
from src.tools import get_categories_list

from src.tui_toolbox import error, warning, progress
from src import get_subcmd_fcts, get_cmd_requires_category

SUBCMD_FCTS = get_subcmd_fcts()
REQUIRES_CAT = get_cmd_requires_category()

def generate_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcmd", help='Commands to manage backups')

    for key, data in SUBCMD_FCTS.items():
        p = subparsers.add_parser(key, help=data[3])
        if key in REQUIRES_CAT.keys():
            p.add_argument("category", help="The category to apply the command", type=str, nargs=1, action="store")
        data[0](p)
    return parser

def validate_args(args, parser):
    if (not args.subcmd) and (not hasattr(args, "category")):
        parser.print_help()
        sys.exit(0)

    if args.subcmd in REQUIRES_CAT and REQUIRES_CAT[args.subcmd]:
        if not args.category[0] in get_categories_list():
            error("Category \"{}\" does not exist".format(args.category[0]))
    if not args.subcmd:
        parser.print_help()
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
    handlers = {key:fct[2] for key, fct in SUBCMD_FCTS.items()}
    return handlers
