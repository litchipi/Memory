#!/usr/bin/env python3
#-*-encoding:utf-8*-

import re
import shutil
import getpass
import json
import sys
import os
import threading
import subprocess

from tui_toolbox import error, warning, progress
from cli import parse_args

TMPDIR = "/tmp/bck_{}".format("TODO_DATE_HERE")
REGISTER_FNAME = "register.json"
BACKUP_DIR = os.path.join(os.path.expanduser("~"), ".backup")
BACKUP_MODES = ["c", "e", "ce", "s"]

THREAD_JOIN_TIMEOUT=0.1
RUNNING_THREADS = {}

__PWD = [threading.Semaphore(), None]

def __get_password():
    global __PWD
    __PWD[0].acquire()
    if __PWD[1] is None:
        __PWD[1] = getpass.getpass()
    __PWD[0].release()
    return __PWD[1]

def check_exist_else_create(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def start(args):
    if not args.subcmd:
        return backup(args)
    elif args.subcmd == "all":
        return backup_all(args)
    elif args.subcmd == "register":
        return register(args)
    elif args.subcmd == "config":
        return config(args)
    else:
        error("Subcommand not recognized: {}".format(args.subcmd))

def __call_cmdline(cmd, **kwargs):
    return subprocess.Popen(re.sub(' +', ' ', cmd).split(" "),shell=False, **kwargs).wait()

def __generate_symlinks(files, wdir):
    for f in files:
        os.symlink(f, os.path.join(wdir, os.path.basename(f)))

def __generate_excludes(excl):
    exclude_dirs = ["--exclude=\"{}/**\"".format(d) for d in excl["dirs"]]
    exclude_files= ["--exclude=\"{}\"".format(f) for f in excl["dirs"]]
    exclude_substr=[] #["--exclude=\"*{}*\"".format(s) for s in excl["substr"]]
    return " ".join([" ".join(e) for e in [exclude_dirs, exclude_files, exclude_substr]])

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

def __archive(outf, arch_dir, incl, excl):
    os.makedirs(arch_dir)
    __generate_symlinks(incl, arch_dir)
    all_excludes = __generate_excludes(excl)
    rootdir = os.path.abspath(arch_dir + "/../")
    ret = __call_cmdline("tar -c -h -v --ignore-command-error -a {} -f {} {}".format(all_excludes, os.path.relpath(outf, rootdir), os.path.relpath(arch_dir, rootdir)),
        cwd=rootdir)
    progress("Return code {} from commandline".format(ret), heading=outf)
    shutil.rmtree(arch_dir, ignore_errors=True) #os.rmdir(arch_dir)
    return ret

def __encrypt(arch):
    ret = __call_cmdline("gpg -c --batch --passphrase {} {}".format(__get_password(), arch))
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

def __start_backup_thread(wdir, mode, exclude, include):
    check_exist_else_create(wdir)
    t = threading.Thread(target=__backup_ops_dispatch(mode), args=(wdir, exclude, include))
    t.start()
    return t
def __wait_backup_finished():
    global RUNNING_THREADS
    while any([t.is_alive() for t in RUNNING_THREADS.values()]):
        for t in RUNNING_THREADS.values():
            t.join(timeout=THREAD_JOIN_TIMEOUT)
        RUNNING_THREADS = {c:t for c, t in RUNNING_THREADS.items() if t.is_alive()}

def __backup_category(args, category):
    rootdir = os.path.join(BACKUP_DIR, category)
    with open(os.path.join(rootdir, REGISTER_FNAME), "r") as f:
        reg = json.load(f)
    
    if "bck" not in reg.keys() or "excl" not in reg.keys():
        error("Register file {} corrupted".format(os.path.join(rootdir, REGISTER_FNAME)))

    global RUNNING_THREADS
    for mode in reg["bck"].keys():
        if len(reg["bck"][mode]) == 0: continue
        RUNNING_THREADS[category + "_" + mode] = __start_backup_thread(os.path.join(TMPDIR, category), mode, reg["excl"], reg["bck"][mode])
def backup_all(args):
    #TODO   BACKUP ALL CATEGORIES
    pass
def backup(args):
    #TODO   Backup everything
    pass

def register(args):
    rootdir = os.path.join(BACKUP_DIR, args.category[0])
    check_exist_else_create(rootdir)

    regfile = os.path.join(rootdir, REGISTER_FNAME)
    if not os.path.isfile(regfile):
        reg = {"excl":{"dirs":[], "files":[]}}
        reg["bck"] = {m:list() for m in BACKUP_MODES}
        with open(regfile, "w") as f:
            json.dump(reg, f)

    with open(regfile, "r") as f:
        reg = json.load(f)

    # Purging paths that doesn't exist anymore
    reg["bck"] = {m:[p for p in l if (os.path.isfile(p) or os.path.isdir(p))] for m, l in reg["bck"].items()}

    for path in args.targets:
        if path in reg["bck"][args.method]:
            warning("Path {} already registered, ignoring ...".format(path))
            continue
        if os.path.isfile(path) or os.path.isdir(path):
            progress("Registered file {}".format(path))
            reg["bck"][args.method].append(str(path.absolute()))
        else:
            warning("Path {} is not a file nor a directory, ignoring...".format(path))

    with open(regfile, "w") as f:
        json.dump(reg, f)

def config(args):
    #TODO   Configure a specific backup stuff
    pass

def __prepare_bck():
    os.mkdir(TMPDIR)

def cleanup():
    if os.path.isdir(TMPDIR):
        if os.path.abspath(TMPDIR)[:5] == '/tmp/':
            shutil.rmtree(TMPDIR, ignore_errors=True)
        else:
            error("Attempt to cleanup folder not located in /tmp/")

if __name__ == "__main__":
    try:
        ret = start(parse_args())
    finally:
        cleanup()
    sys.exit(ret)
