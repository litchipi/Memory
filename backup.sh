#!/bin/bash

read -s -p "Password for encryption: " archive_password
echo ""
make -j$(nproc) ENC_PWD="$archive_password"
make -j$(nproc) finish
