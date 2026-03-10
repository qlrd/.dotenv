#!/bin/bash
filepath="$(cat ~/.cache/helix/file_path_absolute)"
python3 ~/.config/helix/scripts/42header.py "$filepath"
