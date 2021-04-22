#!/usr/bin/env python3
#-*-encoding:utf-8*-

import sys
import os
import json

MODES = ["c", "e", "ce", "s"]

def progress(msg):
    print(" --- {}".format(msg))

def error(msg):
    print("ERROR: {}".format(msg))
    sys.exit(1)

def sanitize_path(path):
    return path.replace(" ", "\\ ")

def read_register(mode, regfile):
    with open(regfile, "r") as f:
        reg = json.load(f)
    something = len(reg[mode]) > 0
    if len(reg[mode]) > 0:
        print(" ".join([sanitize_path(el) for el in reg[mode]]))
    else:
        pass
        #print("nothing")

def start(args):
    if len(args) != 2:
        error("Args expected: <root directory> <mode>")
    if not os.path.isdir(args[0]):
        error("Root directory {} does not exist".format(args[0]))

    if args[1] not in MODES:
        error("Mode {} not recognized. (possible: {})".format(args[1], MODES))

    regfile = os.path.join(args[0], "register.json")
    if not os.path.isfile(regfile):
        error("No register file found")
    
    read_register(args[1], regfile)

if __name__=="__main__":
    start(sys.argv[1:])
