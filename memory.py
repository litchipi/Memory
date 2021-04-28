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

from src.tui_toolbox import error, warning, progress, flow_display
from src.cli import parse_args
from src.backup import backup, backup_all, cleanup
from src.tools import check_exist_else_create
from src.config import config
from src.register import register
from src.exclude import exclude

def start(args):
    if not args.subcmd:
        return backup(args)
    elif args.subcmd == "all":
        return backup_all(args)
    elif args.subcmd == "register":
        return register(args)
    elif args.subcmd == "config":
        return config(args)
    elif args.subcmd == "exclude":
        return exclude(args)
    else:
        error("Subcommand not recognized: {}".format(args.subcmd))

if __name__ == "__main__":
    try:
        ret = start(parse_args())
    finally:
        cleanup()
    sys.exit(ret)
