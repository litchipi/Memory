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
from src.cli import parse_args, get_commands_handlers
from src.backup import backup, backup_all, cleanup
from src.tools import check_exist_else_create
from src.config import config
from src.register import register
from src.exclude import exclude

def start(args):
    handlers = get_commands_handlers()
    if args.subcmd in handlers.keys():
        handlers[args.subcmd](args)
    else:
        error("Subcommand not recognized: {}".format(args.subcmd))

if __name__ == "__main__":
    try:
        start(parse_args())
        ret = 0
    finally:
        cleanup()
        ret = 1
    sys.exit(ret)
