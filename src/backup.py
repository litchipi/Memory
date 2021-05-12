import os
import re
import json
import shutil
import multiprocessing as mproc
import subprocess

from src.tui_toolbox import progress, error, warning
from src.tools import __get_password, check_exist_else_create, load_registry, call_cmdline
from src.tools import GlobalConstants as gcst
from src.register import read_includes
from src.exclude import read_all_excludes, generate_excludes

RUNNING_PROCESSES = {}

def __generate_symlinks(files, wdir):
    for f in files:
        if os.path.isfile(f) or os.path.isdir(f):
            print("{} -> {}".format(f, os.path.join(wdir, os.path.basename(f))))
            os.symlink(f, os.path.join(wdir, os.path.basename(f)))
        else:
            warning("Target {} does not exist anymore, ignoring ...".format(f))

def __backup_ops_dispatch(mode):
    if mode == "ce":
        return __backup_compressed_encrypted
    elif mode == "c":
        return __backup_compressed
    elif mode == "e":
        return __backup_encrypted
    elif mode == "s":
        return __backup_stored
    else:
        error("Cannot find backup operation for mode {}".format(mode))

def __archive(outf, arch_dir, incl, excl, add_args=""):
    os.makedirs(arch_dir)
    __generate_symlinks(incl, arch_dir)
    all_excludes = generate_excludes(excl)
    rootdir = os.path.abspath(arch_dir + "/../")
    ret = call_cmdline("tar -c -h -v --ignore-command-error -a {} -f {} {} {}".format(add_args, 
            os.path.relpath(outf, rootdir),
            all_excludes,
            os.path.relpath(arch_dir, rootdir)
            ),
        cwd=rootdir)
    progress("Return code {} from commandline".format(ret), heading=outf)
    shutil.rmtree(arch_dir, ignore_errors=True) #os.rmdir(arch_dir)
    return ret

def __encrypt(arch):
    ret = call_cmdline("gpg -c --batch --passphrase {} {}".format(__get_password(), arch))
    os.remove(arch)
    return ret

def __backup_stored(wdir, excl, incl, out="stored"):
    ret = __archive(os.path.join(wdir, out + ".tar"), os.path.join(wdir, out), incl, excl)
    if ret != 0: error("{} archive command failed, aborting ...".format(out))

def __backup_compressed(wdir, excl, incl, out="cmp"):
    ret = __archive(os.path.join(wdir, out + ".tar.xz"), os.path.join(wdir, out), incl, excl)
    if ret != 0: error("{} archive command failed, aborting ...".format(out))

def __backup_encrypted(wdir, excl, incl, out="enc"):
    ret = __archive(os.path.join(wdir, out + ".tar"), os.path.join(wdir, out), incl, excl)
    if ret != 0: error("{} archive command failed, aborting ...".format(out))
    ret = __encrypt(os.path.join(wdir, out + ".tar"))
    if ret != 0: error("{} encrypt command failed, aborting ...".format(out))

def __backup_compressed_encrypted(wdir, excl, incl, out="enc_cmp"):
    ret = __archive(os.path.join(wdir, out + ".tar.xz"), os.path.join(wdir, out), incl, excl)
    if ret != 0: error("{} archive command failed, aborting ...".format(out))
    ret = __encrypt(os.path.join(wdir, out + ".tar.xz"))
    if ret != 0: error("{} encrypt command failed, aborting ...".format(out))

def __finish_backup(category):
    ret = call_cmdline("tar -c -h -v --ignore-command-error -a -f {} {}".format(os.path.join(gcst.BACKUP_DIR, category + ".tar"), category), cwd=gcst.TMPDIR)
    progress("Final archive located at \"{}\"".format(os.path.join(gcst.BACKUP_DIR, category + ".tar")), heading=category)
    if ret != 0: error("{} final archive command failed, aborting ...".format(category))

def __start_processes():
    for proc in RUNNING_PROCESSES.values():
        proc.start()

def __create_backup_process(wdir, mode, exclude, include):
    check_exist_else_create(wdir)
    p = mproc.Process(target=__backup_ops_dispatch(mode), args=(wdir, exclude, include))
    return p

def finish_backups(categories):
    processes = list()
    progress("Finalizing backups...")
    for cat in categories:
        if not os.path.isdir(os.path.join(gcst.TMPDIR, cat)): continue
        t = mproc.Process(target=__finish_backup, args=(cat,))
        t.start()
        processes.append(t)
    for t in processes:
        t.join()

def __wait_backup_finished():
    global RUNNING_PROCESSES
    while any([t.is_alive() for t in RUNNING_PROCESSES.values()]):
        for t in RUNNING_PROCESSES.values():
            t.join(timeout=gcst.THREAD_JOIN_TIMEOUT)
        RUNNING_PROCESSES = {c:t for c, t in RUNNING_PROCESSES.items() if t.is_alive()}

def __backup_category(args, category):
    rootdir = os.path.join(gcst.BACKUP_DIR, category)
    reg = load_registry(os.path.join(rootdir, gcst.REGISTER_FNAME))

    global RUNNING_PROCESSES
    for mode in gcst.BACKUP_METHODS:
        incl = read_includes(reg, mode)
        if len(incl) == 0: continue
        if "e" in mode:
            __get_password()
        RUNNING_PROCESSES[category + "_" + mode] = __create_backup_process(os.path.join(gcst.TMPDIR, category), mode, read_all_excludes(reg), incl)

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

    categories = list()
    for _, dirs, _ in os.walk(gcst.BACKUP_DIR):
        for d in [d for d in dirs if os.path.isfile(os.path.join(gcst.BACKUP_DIR, d, gcst.REGISTER_FNAME))]:
            categories.append(d)

    for cat in categories:
        __backup_category(args, cat)
    __start_processes()
    __wait_backup_finished()
    finish_backups(categories)

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
    finish_backups(args.category)

def validate_backup(args):
    pass

def validate_backup_all(args):
    if args.category:
        error("Either backup all or backup some of them")

def generate_backup_parser(parser):
    parser.add_argument('--category', '-c', action='append', help='The name of the category you want to backup')

def generate_backup_all_parser(parser):
    pass
