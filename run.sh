#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  HELL SOCIETY - Quick Launcher (Linux + Termux)                  ║
# ║  Created by: HELL SOCIETY Community                              ║
# ╚══════════════════════════════════════════════════════════════════╝

# Detect platform and use correct python
if [[ "$(uname)" == *"Android"* ]] || [[ "$PREFIX" == *"/data/data/com.termux"* ]]; then
    PYTHON="python3"
else
    PYTHON="python3"
fi

clear

if [ -z "$1" ]; then
    $PYTHON launcher.py
elif [ -f "$1" ]; then
    $PYTHON "$1" "${@:2}"
else
    echo "[!] File not found: $1"
    echo "[i] Usage: ./run.sh [script.py] [args...]"
fi
