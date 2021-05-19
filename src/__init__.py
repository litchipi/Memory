from .backup import validate_backup, generate_backup_parser, backup, validate_backup_all, generate_backup_all_parser, backup_all
from .register import validate_register, generate_register_parser, register
from .config import validate_config, generate_config_parser, config
from .exclude import validate_exclude, generate_exclude_parser, exclude
from .edit import validate_edit, generate_edit_parser, edit
from .check import validate_check, generate_check_parser, check

def get_subcmd_fcts():
    return {
        "backup": [generate_backup_parser, validate_backup, backup, "Backup one or more categories"],
        "all": [generate_backup_all_parser, validate_backup_all, backup_all, "Backup all categories"],
        "register": [generate_register_parser, validate_register, register, "Register new files / folders for backup"],
        "exclude": [generate_exclude_parser, validate_exclude, exclude, "Exclude files / folders for backup"],
        "config": [generate_config_parser, validate_config, config, "Configure backup tool"],
        "edit": [generate_edit_parser, validate_edit, edit, "Edit register of a category"],
        "check": [generate_check_parser, validate_check, check, "Check if a backup needs to be done again"],
        }

