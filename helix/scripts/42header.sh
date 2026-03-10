#!/bin/bash
filepath="$(cat ~/.cache/helix/file_path_absolute | tr -d '\n')"

if [[ -z "$filepath" ]]; then
    echo "42header: could not read filepath from cache" >&2
    exit 1
fi

# Make absolute if relative
if [[ "$filepath" != /* ]]; then
    filepath="$(realpath -- "$filepath" 2>/dev/null)"
fi

if [[ -z "$filepath" ]]; then
    echo "42header: could not resolve absolute path" >&2
    exit 1
fi

python3 ~/.config/helix/scripts/42header.py "$filepath"
