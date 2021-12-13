#restic forget --keep-last 1 --prune

#--keep-last n never delete the n last (most recent) snapshots
#--keep-hourly n for the last n hours in which a snapshot was made, keep only the last snapshot for each hour.
#--keep-daily n for the last n days which have one or more snapshots, only keep the last one for that day.
#--keep-weekly n for the last n weeks which have one or more snapshots, only keep the last one for that week.
#--keep-monthly n for the last n months which have one or more snapshots, only keep the last one for that month.
#--keep-yearly n for the last n years which have one or more snapshots, only keep the last one for that year.

from src.tui_toolbox import error, warning, progress
from src.tools import *
from src.tools import GlobalConstants as gcst

PRUNE_COMMON_ARGS = " ".join([
    "--prune",
    "--no-cache",
    "--group-by host",
    ])

### CLI
def prune_all(args):
    for cat in get_categories_list():
        progress("Pruning category {}, keeping only {} snapshots".format(cat, args.keep))
        repo_path = get_category_repodir(cat)
        call_cmdline("RESTIC_PASSWORD_FILE={} restic -r {} forget --keep-last {} {}".format(
            gcst.MEMORY_PWD, repo_path, args.keep, PRUNE_COMMON_ARGS))
    progress("Done")

def prune(args):
    #call_cmdline(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kwargs):
    for cat in args.category:
        progress("Pruning category {}, keeping only {} snapshots".format(cat, args.keep))
        repo_path = get_category_repodir(cat)
        call_cmdline("RESTIC_PASSWORD_FILE={} restic -r {} forget --keep-last {} {}".format(
            gcst.MEMORY_PWD, repo_path, args.keep, PRUNE_COMMON_ARGS))
        progress("Done")

def generate_prune_parser(parser):
    parser.add_argument("--keep", "-k", type=int,
            help="Number of snapshots to keep (from most recent ones)", default=1)

def validate_prune(args):
    if args.keep < 1:
        error("Must keep at least 1 snapshot")
