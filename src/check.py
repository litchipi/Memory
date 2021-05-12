import os

from src.tools import GlobalConstants as gcst
from src.tools import setup_default_registry, load_registry
from src.register import read_includes
from src.tui_toolbox import error, progress, warning

def check_need_backup(last_backup_time, target):
    return int(os.path.getmtime(target)*1000) > last_backup_time

def __check_targets_need_backup(last_backup_time, incl):
    for target in incl:
        if check_need_backup(last_backup_time, target):
            return True
    return False

def check(args):
    need_do_again = {cat:{mode:False for mode in gcst.BACKUP_METHODS} for cat in args.category}
    for cat in args.category:
        rootdir = os.path.join(gcst.BACKUP_DIR, cat)
        regfile = os.path.join(rootdir, gcst.REGISTER_FNAME)
        if not os.path.isfile(regfile):
            setup_default_registry(regfile)
        reg = load_registry(regfile)
        
        for mode in gcst.BACKUP_METHODS:
            incl = read_includes(reg, mode)
            for target in incl:
                if check_need_backup(reg["last_backup"], target):
                    need_do_again[cat][mode] = True
                    break
            if need_do_again[cat][mode]:
                progress("Need a new backup for mode \"{}\"".format(mode), heading=cat)
    return need_do_again

def generate_check_parser(parser):
    parser.add_argument('--category', '-c', action='append', help='The name of the category(ies) you want to check')

def validate_check(args):
    if not args.category:
        error("Requires a category for action \"{}\"".format(args.subcmd))
