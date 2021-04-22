#!/bin/bash

if [ $# -lt 2 ] ; then
    echo "Usage: $(basename $0) <type> <exclude> [exclude] ..."
    echo -e "Types:\n\tfiles\n\tdirs\n"
    exit 1;
fi

ROOT=$HOME/.backup
TYPE=$1
shift
mkdir -p $ROOT
python3 ./register_forbidden.py $ROOT $TYPE "$@"
