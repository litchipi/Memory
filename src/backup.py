import os
import re
import json
import shutil
import multiprocessing as mproc
import subprocess

from src.tui_toolbox import progress, error, warning
from src.tools import GlobalConstants as gcst
from src.tools import __get_password, check_exist_else_create, load_registry, call_cmdline, get_current_time, write_registry, sanitize_path, get_categories_list
from src.register import read_includes
from src.exclude import read_all_excludes, generate_excludes
from src.check import __check_targets_need_backup

RUNNING_PROCESSES = {}

def __restic_backup(category, excl, incl):
    all_excludes = generate_excludes(excl)
    out_repo = os.path.join(gcst.BACKUP_DIR, category)
    if not os.path.exists(os.path.join(out_repo, "config")):
        progress("Init restic repository...", heading=category)
        if not os.path.isdir(out_repo):
            os.mkdir(out_repo)
        ret = call_cmdline("RESTIC_PASSWORD={} restic init -r {}".format(__get_password(), out_repo))
    progress("Backup in progress...", heading=category)
    ret = call_cmdline("RESTIC_PASSWORD={} restic backup -r {} {} -- {}".format(
        __get_password(), out_repo , all_excludes, " ".join([p for p in incl if os.path.exists(p)])))
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
    rootdir = os.path.join(gcst.BACKUP_DIR, category)
    reg_fname = os.path.join(rootdir, gcst.REGISTER_FNAME)
    reg = load_registry(reg_fname)

    global RUNNING_PROCESSES
    incl = read_includes(reg)
    excl = read_all_excludes(reg)
    if len(incl) == 0: return
    __get_password()
    RUNNING_PROCESSES[category] = __create_backup_process(category, excl, incl)

def __prepare_bck():
    os.mkdir(gcst.TMPDIR)

def cleanup():
    if os.path.isdir(gcst.TMPDIR):
        if os.path.abspath(gcst.TMPDIR)[:5] == '/tmp/':
            shutil.rmtree(gcst.TMPDIR, ignore_errors=True)
        else:
            error("Attempt to cleanup folder not located in /tmp/")




##### CLI

def backup_all(args):
    __prepare_bck()

    categories = get_categories_list()

    for cat in categories:
        __backup_category(args, cat)
    __start_processes()
    __wait_backup_finished()

def backup(args):
    __prepare_bck()
    for cat in args.category:
        if not os.path.isdir(os.path.join(gcst.BACKUP_DIR, cat)):
            warning("Category {} doesn't exist, ignoring ...".format(cat))
        elif not os.path.isfile(os.path.join(gcst.BACKUP_DIR, cat, gcst.REGISTER_FNAME)):
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
