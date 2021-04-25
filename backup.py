#!/usr/bin/env python3
#-*-encoding:utf-8*-

import shutil
import json
import sys
import os

from tui_toolbox import error, warning, progress
from cli import parse_args

TMPDIR = "/tmp/bck_{}".format("TODO_DATE_HERE")
REGISTER_FNAME = "register.json"
BACKUP_DIR = os.path.join(os.path.expanduser("~"), ".backup")
BACKUP_MODES = ["c", "e", "ce", "s"]

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
