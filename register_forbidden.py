#!/usr/bin/env python3
#-*-encoding:utf-8*-

import sys
import os
import json

TYPES= ["dirs", "files"]

def progress(msg):
    print(" --- {}".format(msg))

def warning(msg):
    print(" /!\ {}".format(msg))

def error(msg):
    print("ERROR: {}".format(msg))
    sys.exit(1)

def register_exclusion(relative_root, t, register_file, rules):
    with open(register_file, "r") as f:
        reg = json.load(f)

    # Purging paths that doesn't exist anymore
    reg["bck"] = {m:[p for p in l if (os.path.isfile(p) or os.path.isdir(p))] for m, l in reg["bck"].items()}

    for r in rules:
        if r in reg["excl"][t]:
            warning("Rule {} already in {} exclusion, ignoring...".format(r, t))
        reg["excl"][t].append(r)
        progress("Added rule {} to {} exclusion".format(r, t))

    with open(register_file, "w") as f:
        json.dump(reg, f)

def start(args):
    if len(args) < 3:
        error("Args expected: <root directory> <type> <excl> [excl] ...")

    if not os.path.isdir(args[0]):
        error("Root directory {} does not exist".format(args[0]))

    if args[1] not in TYPES:
        error("Type {} not recognized. (possible: {})".format(args[1], TYPES))

    regfile = os.path.join(args[0], "register.json")
    if not os.path.isfile(regfile):
        error("No register file {} found".format(regfile))
    register_exclusion(args[0], args[1], regfile, args[2:])

start(sys.argv[1:])
