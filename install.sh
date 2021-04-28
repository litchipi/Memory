INSTALL_DIR=~/.local/share/backup/

mkdir -p $INSTALL_DIR/
cp -r ./memory.py ./src/ $INSTALL_DIR/
ln -s $INSTALL_DIR/memory.py ~/.local/bin/memory
