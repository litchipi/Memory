import os

from src.tools import GlobalConstants as gcst
from src.tools import *
from src.register import read_includes
from src.tui_toolbox import error, progress, warning

def check_dir_need_backup(last_backup_time, dtarget, dexcl):
    for root, dirs, _ in os.walk(dtarget):
        for d in dirs:
            if d in dexcl: continue
            if int(os.path.getmtime(os.path.join(root, d))*1000) > last_backup_time:
                return True
    return False

def check_need_backup(last_backup_time, target, dir_excludes):
    if os.path.isdir(target):
        return check_dir_need_backup(last_backup_time, target, dir_excludes)
    if not os.path.isfile(target):
        return False
    return int(os.path.getmtime(target)*1000) > last_backup_time

def __check_targets_need_backup(last_backup_time, incl, dir_excludes):
    for target in incl:
        if not os.path.exists(target):
            warning("Target {} does not exist, skipping ...".format(target))
            continue
        if check_need_backup(last_backup_time, target, dir_excludes):
            return True
    return False

#TODO   Does not work properly
def check(args):
    new_bck = False
    need_do_again = {cat:False for cat in args.category}
    for cat in args.category:
        reg = load_category_registry(cat, create=True)
        
        incl = read_includes(reg)
        for target in incl:
            if check_need_backup(reg["last_backup"], target, reg[gcst.EXCLUDE_TEXT]["dirs"]):
                need_do_again[cat] = True
                break
        if need_do_again[cat]:
            progress("Need a new backup", heading=cat)
            new_bck = True

    if not new_bck:
        progress("No categories need any new backup")
    return need_do_again

def generate_check_parser(parser):
    pass

def validate_check(args):
    if not args.category:
        error("Requires a category for action \"{}\"".format(args.subcmd))
