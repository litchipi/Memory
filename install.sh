#!/bin/bash

function no_output {
	$@ 1>/dev/null 2>/dev/null
}

function test_dep {
	if ! no_output dpkg -s $1; then
		echo "Dependency $1 need to be installed"
		echo -e "\tsudo apt install $1"
		return 1;
	fi
	return 0;
}

test_dep "restic"

INSTALL_DIR=~/.local/share/memory/

mkdir -p $INSTALL_DIR/
cp -r ./memory.py ./src/ $INSTALL_DIR/
rm -f ~/.local/bin/memory
ln -s $INSTALL_DIR/memory.py ~/.local/bin/memory
