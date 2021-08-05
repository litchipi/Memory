import os
import re
import json
import shutil
import multiprocessing as mproc
import subprocess

from src.tui_toolbox import progress, error, warning, debug
from src.tools import GlobalConstants as gcst
from src.tools import *
from src.register import read_includes
from src.exclude import read_all_excludes, generate_excludes
from src.check import __check_targets_need_backup

RUNNING_PROCESSES = {}

def __restic_backup(category, excl, incl):
    all_excludes = generate_excludes(excl)
    out_repo = get_category_repodir(category)
    if not os.path.exists(os.path.join(out_repo, "config")):
        progress("Init restic repository...", heading=category)
        if not os.path.isdir(out_repo):
            os.mkdir(out_repo)
        ret = call_cmdline("RESTIC_PASSWORD={} restic init -r {}".format(get_password(), out_repo))
    progress("Backup in progress...", heading=category)
    ret = call_cmdline("RESTIC_PASSWORD={} restic backup -r {} {} -- {}".format(
        get_password(), out_repo , all_excludes, " ".join([p for p in incl if os.path.exists(p)])))
    if ret:
        error("Restic command failed for category {}".format(category))

    progress("Success", heading=category)

def __start_processes():
    for proc in RUNNING_PROCESSES.values():
        proc.start()

def __create_backup_process(category, exclude, include):
    return mproc.Process(target=__restic_backup, args=(category, exclude, include))

def __wait_backup_finished():
    global RUNNING_PROCESSES
    while any([t.is_alive() for t in RUNNING_PROCESSES.values()]):
        for t in RUNNING_PROCESSES.values():
            t.join(timeout=gcst.THREAD_JOIN_TIMEOUT)
        RUNNING_PROCESSES = {c:t for c, t in RUNNING_PROCESSES.items() if t.is_alive()}

def __backup_category(args, category):
    debug("Loading registry ...", heading=category)
    reg = load_category_registry(category, create=False)

    global RUNNING_PROCESSES
    debug("Loading includes ...", heading=category)
    incl = read_includes(reg)
    debug("Loading excludes ...", heading=category)
    excl = read_all_excludes(reg)
    if len(incl) == 0: return
    get_password()
    debug("Starting process ...", heading=category)
    RUNNING_PROCESSES[category] = __create_backup_process(category, excl, incl)




##### CLI
def backup_all(args):
    categories = get_categories_list()

    for cat in categories:
        __backup_category(args, cat)
    __start_processes()
    __wait_backup_finished()

def backup(args):
    for cat in args.category:
        if not os.path.isdir(get_category_repodir(cat)):
            warning("Category {} doesn't exist, ignoring ...".format(cat))
        elif not os.path.isfile(get_category_registry_fname(cat)):
            warning("Category {} doesn't have a register, ignoring ...".format(cat))
        else:
            __backup_category(args, cat)
    __start_processes()
    __wait_backup_finished()

def validate_backup(args):
    pass

def validate_backup_all(args):
    pass

def generate_backup_parser(parser):
    parser.add_argument('--force', '-f', help='Force backup even if doesn\'t need to', action="store_true")

def generate_backup_all_parser(parser):
    parser.add_argument('--force', '-f', help='Force backup even if doesn\'t need to', action="store_true")
