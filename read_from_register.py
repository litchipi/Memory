#!/usr/bin/env python3
#-*-encoding:utf-8*-

import sys
import os
import json

WHAT = ["include", "exclude"]
TYPES = ["files", "dirs"]
MODES = ["c", "e", "ce", "s"]

def progress(msg):
    print(" --- {}".format(msg))

def error(msg):
    print("ERROR: {}".format(msg))
    sys.exit(1)

def sanitize_path(path):
    return path.replace(" ", "\\ ")

def read_include_register(mode, regfile):
    with open(regfile, "r") as f:
        reg = json.load(f)
    print(" ".join([sanitize_path(el) for el in reg["bck"][mode]]))

def read_exclude_register(t, regfile):
    with open(regfile, "r") as f:
        reg = json.load(f)
    print(" ".join([sanitize_path(el) for el in reg["excl"][t]]))

def start_exclude(args, regfile):
    if args[2] not in TYPES:
        error("Mode {} not recognized. (possible: {})".format(args[2], MODES))

    read_exclude_register(args[2], regfile)

def start_include(args, regfile):
    if args[2] not in MODES:
        error("Mode {} not recognized. (possible: {})".format(args[2], MODES))

    read_include_register(args[2], regfile)

def start(args):
    if len(args) != 3:
        error("Args expected: <root directory> <what> <mode/type>")

    if not os.path.isdir(args[0]):
        error("Root directory {} does not exist".format(args[0]))

    if args[1] not in WHAT:
        error("What {} not recognized. (possible {})".format(args[1], WHAT))
    
    regfile = os.path.join(args[0], "register.json")
    if not os.path.isfile(regfile):
        error("No register file found")
    

    if args[1] == "exclude":
        start_exclude(args, regfile)
    elif args[1] == "include":
        start_include(args, regfile)

if __name__=="__main__":
    start(sys.argv[1:])
