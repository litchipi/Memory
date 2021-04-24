#TODO   Copy the necessary files into an install directory
#       Create aliases for quick setup
echo -e "#!/bin/bash\ncd $PWD\n./register_to_exclusion.sh \$@" > ~/.local/bin/bck_exclude
chmod +x ~/.local/bin/bck_exclude

echo -e "#!/bin/bash\nOLD_DIR=\$PWD\ncd $PWD\n./register_to_backup.sh \$OLD_DIR \$@" > ~/.local/bin/bck_register
chmod +x ~/.local/bin/bck_register

echo -e "#!/bin/bash\ncd $PWD\n./backup.sh \$@" > ~/.local/bin/backup
chmod +x ~/.local/bin/backup
