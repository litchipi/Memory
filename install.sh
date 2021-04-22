echo -e "#!/bin/bash\ncd $PWD\n./register_to_backup.sh \$@" >> ~/.local/bin/bck_register
chmod +x ~/.local/bin/bck_register

echo -e "#!/bin/bash\ncd $PWD\n./backup.sh \$@" >> ~/.local/bin/backup
chmod +x ~/.local/bin/backup
