import os
import re
import toml
import time
import string
import random
import shutil
import getpass
import threading
import subprocess

from src.tui_toolbox import error, warning, progress

class GlobalConstants:
    TMPDIR = "/tmp/bck_{}".format("TODO_DATE_HERE")
    REGISTER_FNAME = "register.toml"
    BACKUP_DIR = os.path.join(os.path.expanduser("~"), ".backup")
    BACKUP_METHODS = ["c", "e", "ce", "s"]
    EXCLUDES_TYPES = ["files", "dirs", "substr"]
    THREAD_JOIN_TIMEOUT=0.1
    EDITOR_CMD = "vim "
    CONFIG_FORBIDDEN_CHARS = "{}[],;"
    DEFAULT_CAT_CONFIG = {}
    INCLUDE_TEXT = "include"
    EXCLUDE_TEXT = "exclude"
    DEFAULT_CAT_REGISTER = {INCLUDE_TEXT:{m:list() for m in BACKUP_METHODS}, EXCLUDE_TEXT:{t:list() for t in EXCLUDES_TYPES}}
    DEFAULT_SUBCMD = "backup"

__PWD = [threading.Semaphore(), None]

def check_category_exist(cat):
    return os.path.isdir(os.path.join(GlobalConstants.BACKUP_DIR, cat))

def __get_password():
    global __PWD
    __PWD[0].acquire()
    if __PWD[1] is None:
        __PWD[1] = getpass.getpass()
    __PWD[0].release()
    return __PWD[1]

def check_exist_else_create(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def call_cmdline(cmd, **kwargs):
    #return subprocess.Popen(__prep_popen_cmd(cmd).split(" "),shell=False, **kwargs).wait()
    return subprocess.Popen(__prep_popen_cmd(cmd), shell=True, **kwargs).wait()

def __prep_popen_cmd(cmd):
    return re.sub(' +', ' ', cmd)

def get_tmp_dir(k=20):
    dirname = "mem." + "".join(random.choices(string.ascii_lowercase + string.digits, k=k))
    os.mkdir(os.path.join("/tmp/", dirname))
    return dirname

def rm_tmp_dir(dirname):
    if dirname[:4] == "mem.":
        shutil.rmtree(os.path.join("/tmp/", dirname))
    else:
        error("Attempt to remove directory not temporary")

######## EDIT PLAINTEXT TO TOML

def extract_from_file(fname):
    with open(fname, "r") as f:
        return toml.load(f)

def export_to_file(fname, data):
    with open(fname, "w") as f:
        toml.dump(data, f)

def edit_list_in_plaintext(fname, keys_names, name="unknown", recurs=0, dirname=None, **kwargs):
    if len(keys_names) > 1:
        data = extract_from_file(fname)
        key_name = keys_names.pop(0)
        if key_name not in data.keys():
            error("Key {} not found in \"{}\" config file (recursion {})".format(key_name, name, recurs))
        if dirname is None:
            dirname = get_tmp_dir()
        
        tmp_fname = os.path.join("/tmp/", dirname, key_name)
        export_to_file(tmp_fname, data[key_name])
        ret = edit_list_in_plaintext(tmp_fname, keys_names, name=name, recurs=recurs+1, dirname=dirname, **kwargs)
        
        data[key_name] = extract_from_file(tmp_fname)
        rm_tmp_dir(dirname)
        export_to_file(fname, data)
        return ret
    elif len(keys_names) == 1:
        ret = __edit_list_in_plaintext(fname, keys_names[0], name=name, **kwargs)
    else:
        error("No keys passed as arguments")
    return ret

def __edit_list_in_plaintext(fname, key_name, name="unknown", **kwargs):
    data = extract_from_file(fname)
    if key_name not in data.keys():
        error("Key {} not found in \"{}\" config file, cannot edit".format(key_name, name))
 
    tmpdir = get_tmp_dir()
    tmp_fname = os.path.join("/tmp/", tmpdir, key_name)
    dump_to_user(tmp_fname, data[key_name])

    call_cmdline(GlobalConstants.EDITOR_CMD + tmp_fname)

    user_input = load_user_input(tmp_fname, **kwargs)
    rm_tmp_dir(tmpdir)
    data[key_name] = user_input
    export_to_file(fname, data)
    return data

def validate_dump_to_user(data):
    if type(data) != list:
        error("Cannot edit other configurations than simple string lists")

def dump_to_user(fname, data):
    validate_dump_to_user(data)
    with open(fname, "w") as f:
        f.write("\n".join(data))

def load_user_input(fname, validate_fct=lambda f: True, transform_fct=lambda f: f):
    with open(fname, "r") as f:
        datas = f.read()
    __validate_load_userinp(datas)
    data = [transform_fct(l) for l in datas.split("\n")]
    return [l for l in data if l != "" and validate_fct(l)]

def __validate_load_userinp(data):
    if any([f in data for f in GlobalConstants.CONFIG_FORBIDDEN_CHARS]):
        error("Error while loading user configuration, forbidden char used")
    data.replace("\\ ", " ").replace(" ", "\\ ")



########" Configuration

def update_config(cfg_fname, key_name, data):
    with open(cfg_fname, "r") as f:
        parsed_toml = toml.load(f)
    try:
        parsed_toml[key_name] = data
    except KeyError:
        error("Config name \"{}\" does not exist in configuration".format(key_name))
    with open(cfg_fname, "w") as f:
        toml.dump(parsed_toml, f)

def extract_from_config(cfg_fname, key_name):
    with open(cfg_fname, "r") as f:
        parsed_toml = toml.load(f)
    try:
        parsed_toml[key_name]
    except KeyError:
        error("Config name \"{}\" does not exist in configuration".format(key_name))



########## Registry

def get_current_time():
    return int(time.time()*1000)

def setup_default_registry(fname):
    default = dict.copy(GlobalConstants.DEFAULT_CAT_REGISTER)
    default["last_backup"] = get_current_time()
    with open(fname, "w") as f:
        toml.dump(default, f)

def write_registry(fname, reg):
    with open(fname, "w") as f:
        toml.dump(reg, f)

def load_registry(fname):
    with open(fname, "r") as f:
        reg = toml.load(f)
    __validate_register(reg)
    if "last_backup" not in reg.keys():
        reg["last_backup"] = 0
        write_registry(fname, reg)
    return reg

def __validate_register(reg):
    if (GlobalConstants.INCLUDE_TEXT not in reg.keys()) or (GlobalConstants.EXCLUDE_TEXT not in reg.keys()):
        error("Register file corrupted")
