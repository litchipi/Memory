#!/usr/bin/env python3
#-*-encoding:utf-8*-

import sys
import os
import json

MODES = ["c", "e", "ce", "s"]

def progress(msg):
    print(" --- {}".format(msg))

def warning(msg):
    print(" /!\ {}".format(msg))

def error(msg):
    print("ERROR: {}".format(msg))
    sys.exit(1)

def register_all(relative_root, mode, register_file, pathlist):
    with open(register_file, "r") as f:
        reg = json.load(f)

    # Purging paths that doesn't exist anymore
    reg["bck"] = {m:[p for p in l if (os.path.isfile(p) or os.path.isdir(p))] for m, l in reg["bck"].items()}

    for rel_path in pathlist:
        path = os.path.abspath(os.path.join(relative_root, rel_path))
        if path in reg["bck"][mode]:
            warning("Path {} already registered, ignoring ...".format(path))
            continue
        if os.path.isfile(path) or os.path.isdir(path):
            progress("Registered file {}".format(path))
            reg["bck"][mode].append(path)
        else:
            warning("Path {} is not a file nor a directory, ignoring...".format(path))

    with open(register_file, "w") as f:
        json.dump(reg, f)

def start(args):
    if len(args) < 3:
        error("Args expected: <old_dir> <root directory> <mode> <file> [file] ...")

    if not os.path.isdir(args[0]):
        error("Old PWD dir {} does not exist".format(args[0]))
    if not os.path.isdir(args[1]):
        error("Root directory {} does not exist".format(args[1]))

    if args[2] not in MODES:
        error("Mode {} not recognized. (possible: {})".format(args[2], MODES))

    regfile = os.path.join(args[1], "register.json")
    if not os.path.isfile(regfile):
        reg = {"excl":{"dirs":[], "files":[]}}
        reg["bck"] = {m:list() for m in MODES}
        with open(regfile, "w") as f:
            json.dump(reg, f)
    register_all(args[0], args[2], regfile, args[3:])

start(sys.argv[1:])
