import os

from src.tui_toolbox import error, warning, progress
from src.tools import GlobalConstants as gcst
from src.tools import *

def edit(args):
    regfile = get_category_registry_fname(args.category[0])
    if not os.path.isfile(regfile):
        setup_default_registry(regfile)
    call_cmdline(gcst.EDITOR_CMD + regfile, stdout=None, stderr=None)

def generate_edit_parser(parser):
    sub = parser.add_subparsers(dest="edit_cmd", help="Edit the register of a category")
    parser.add_argument('--category', '-c', action='append', help='The name of the category you want to backup')

def validate_edit(args):
    if not args.category or len(args.category) > 1:
        error("Requires a category for action \"{}\"".format(args.subcmd))
    if not check_category_exist(args.category[0]):
        error("Category {} does not exist".format(args.category[0]))
