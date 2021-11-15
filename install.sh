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

test_dep "restic" || exit 1;
test_dep "python3-pip" || exit 1;

pip install argcomplete argparse toml argon2

INSTALL_DIR=~/.local/share/memory/

mkdir -p $INSTALL_DIR/ ~/.local/bin ~/.local/bin
cp -r ./memory.py ./src/ $INSTALL_DIR/
rm -f ~/.local/bin/memory
ln -s $INSTALL_DIR/memory.py ~/.local/bin/memory

if ! echo $PATH | grep "$HOME/.local/bin"; then
	echo "Add ~/.local/bin to PATH"
	echo "export PATH=$PATH:$HOME/.local/bin" >> ~/.bashrc
fi

echo ''
echo 'Done'
