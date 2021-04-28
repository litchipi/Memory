def read_excludes(reg, excl):
    if excl not in reg["exclude"].keys():
        return []
    else:
        return reg["exclude"][excl]

def read_all_excludes(reg):
    return reg["exclude"]

def generate_excludes(excl):
    for key in ["dirs", "files", "substr"]:
        if key not in excl.keys():
            excl[key] = []
    exclude_dirs = ["--exclude=\"{}/**\"".format(d) for d in excl["dirs"]]
    exclude_files= ["--exclude=\"{}\"".format(f) for f in excl["files"]]
    exclude_substr=["--exclude=\"*{}*\"".format(s) for s in excl["substr"]]
    return " ".join([" ".join(e) for e in [exclude_dirs, exclude_files, exclude_substr]])



def exclude(args):
    #TODO   Exclude a file / dir / substr / other & create rule for tar exclusion
    pass

def generate_exclude_parser(parser):
    parser.add_argument('--category', '-c', action='append', help='The name of the category you want to backup')

def validate_exclude(args):
    pass
