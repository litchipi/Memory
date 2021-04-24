import argparse

from tui_toolbox import error

def generate_parser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--all', '-a', help="Backup everything", action="store_true")
    parser.add_argument('--category', '-c', action='append', help='The name of the category you want to backup')

    subparsers = parser.add_subparsers(dest="subcmd", help='Commands to manage backups')
    
    parser_register = subparsers.add_parser('register', help='Register new files / folders for backup')
    __generate_register_parser(parser_register)
    
    parser_config = subparsers.add_parser('config', help='Edit rules of backup')
    __generate_config_parser(parser_config)

    return parser

def __generate_config_parser(parser):
    sub = parser.add_subparsers(dest="config_cmd", help="Quick config commands")
    exclude = sub.add_parser("exclude", help="Exclude a particular file or dir")
    add_rule = sub.add_parser("add_rule", help="Add a rule applied to every possible files")
    edit = sub.add_parser("edit", help="Edit rules")

def __generate_register_parser(parser):
    #TODO   Add argument for what method to use to store the file
    pass

def validate_args(args, parser):
    if not args.subcmd:
        if (not args.all) and (not args.category):
            error("Requires at least 1 category name (or '--all'/'-a' flag) or a subcommand", help_msg=parser.format_help())
        if args.all and args.category:
            error("Either backup all or backup some of them", help_msg=parser.format_help())
    elif args.subcmd in ["register", "config"]:
        if args.all:
            error("Cannot perform \"{}\" action on all categories".format(args.subcmd))
        if not args.category:
            error("Requires a category for action \"{}\"".format(args.subcmd))
        if len(args.category) > 1:
            error("Cannot perform \"{}\" action on more than 1 category".format(args.subcmd))

def parse_args():
    parser = generate_parser()
    args = parser.parse_args()
    validate_args(args, parser)
    print(args)
    return args
