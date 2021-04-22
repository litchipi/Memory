#!/bin/bash

if [ $# -lt 2 ] ; then
    echo "Usage: $(basename $0) <old_dir> <mode> <file(s)>"
    echo -e "Modes:\n\tc:  Compressed\n\te:  Encrypted\n\tce: Compressed + Encrypted\n\ts:  Stored only\n"
    exit 1;
fi

ROOT=$HOME/.backup
MODE=$2
OLD_DIR=$1
shift
shift
mkdir -p $ROOT
python3 ./register_file.py $OLD_DIR $ROOT $MODE "$@"
