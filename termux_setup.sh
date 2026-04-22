#!/data/data/com.termux/files/usr/bin/bash

# SOLMATES Termux Setup Script
# Run this once on your phone to start the auto-sync

echo "--- Installing Python and Dependencies ---"
pkg update -y
pkg install -y python ndk-sysroot clang make libffi openssl

# Ensure we have pip
python -m ensurepip

echo "--- Starting SOLMATES Auto-Sync ---"
# Run the python script which handles the rest
python termux_sync.py
