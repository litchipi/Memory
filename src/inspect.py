import os
import argparse

from src.tui_toolbox import error, warning, progress, create_style
from src.tools import GlobalConstants as gcst
from src.tools import *

def gather_more_info(path, catlist):
    latest_snapshots = [(cat, os.path.getmtime(get_output_latest_snapshot(cat))) for cat in catlist]
    sorted(latest_snapshots, key=lambda x: x[1], reverse=True)

    time_format = "%d/%m/%y %H:%M:%S"
    print("Latest snapshot: {} ({})".format(latest_snapshots[0][0],
        time.strftime(time_format, time.gmtime(latest_snapshots[0][1]))
        ))

def __inspect_path(path, info):
    cat_which_incl = list()
    for cat in get_categories_list():
        reg = load_category_registry(cat)
        for incl in reg[gcst.INCLUDE_TEXT]:
            incl = os.path.abspath(incl)

            if path == incl:
                cat_which_incl.append(cat)
            elif os.path.isdir(incl):
                if incl + "/" in path:
                    cat_which_incl.append(cat)

    if len(cat_which_incl) == 0:
        print("Not registered for backup")
    else:
        print("Included in categories" +
                create_style(color="yellow", effect="bold"),
                ", ".join(cat_which_incl),
                create_style())

        if info:
            gather_more_info(path, cat_which_incl)




### CLI
def inspect(args):
    if not args.list or (not os.path.isdir(args.path)):
        __inspect_path(args.path, args.info)
    else:
        for d in os.listdir(args.path):
            print(d)
            __inspect_path(os.path.join(args.path, d), args.info)
            print("")

def generate_inspect_parser(parser):
    parser.add_argument("path", type=str, help="The path to inspect")
    parser.add_argument("-i", "--info", action="store_true",
            help="Gather additionnal informations about the path")
    parser.add_argument("-l", "--list", action="store_true",
            help="Inspect every elements inside the given path")

def validate_inspect(args):
    if os.path.exists(args.path):
        args.path = os.path.abspath(args.path)
