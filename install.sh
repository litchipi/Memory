INSTALL_DIR=~/.local/share/memory/

mkdir -p $INSTALL_DIR/
cp -r ./memory.py ./src/ $INSTALL_DIR/
rm -f ~/.local/bin/memory
ln -s $INSTALL_DIR/memory.py ~/.local/bin/memory
