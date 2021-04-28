import sys
import pathlib
import argparse

from src.tui_toolbox import error, warning, progress
from src.backup import validate_backup, generate_backup_parser
from src.register import validate_register, generate_register_parser
from src.config import validate_config, generate_config_parser
from src.exclude import validate_exclude, generate_exclude_parser

def generate_parser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--category', '-c', action='append', help='The name of the category you want to backup')

    subparsers = parser.add_subparsers(dest="subcmd", help='Commands to manage backups')
    parser_all = subparsers.add_parser('all', help='Backup all categories')

    generate_backup_parser(parser)
    generate_register_parser(subparsers.add_parser('register', help='Register new files / folders for backup'))
    generate_exclude_parser(subparsers.add_parser("exclude", help="Exclude files / folders for backup"))
    generate_config_parser(subparsers.add_parser('config', help='Edit rules of backup'))
    
    return parser

def validate_args(args, parser):
    if (not args.subcmd) and (not args.category):
        parser.print_help()
        sys.exit(0)

    if args.subcmd == "all" or not args.subcmd:
        validate_backup(args)
    
    elif args.subcmd == "register":
        validate_register(args)

    elif args.subcmd == "config":
        validate_config(args)

    elif args.subcmd == "exclude":
        validate_exclude(args)

def parse_args():
    parser = generate_parser()
    args = parser.parse_args()
    validate_args(args, parser)
    return args
