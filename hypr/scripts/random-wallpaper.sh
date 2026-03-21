#!/bin/sh

WALLS_DIR="$HOME/.config/hypr/walls"
INTERVAL=3600
CURRENT=""

# Get the active monitor name
MONITOR=$(hyprctl monitors -j | grep '"name"' | head -n 1 | cut -d'"' -f4)

while true; do
    # Get all image files
    WALLPAPERS=$(find "$WALLS_DIR" -maxdepth 1 -type f \( -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.webp' \))

    # Count them
    COUNT=$(echo "$WALLPAPERS" | wc -l)

    if [ "$COUNT" -eq 0 ]; then
        sleep "$INTERVAL"
        continue
    fi

    # Pick a random wallpaper, avoiding the current one
    PICK="$CURRENT"
    while [ "$PICK" = "$CURRENT" ] && [ "$COUNT" -gt 1 ]; do
        PICK=$(echo "$WALLPAPERS" | shuf -n 1)
    done

    # If only one wallpaper, just use it
    if [ "$COUNT" -eq 1 ]; then
        PICK=$(echo "$WALLPAPERS" | head -n 1)
    fi

    # Apply via hyprctl
    hyprctl hyprpaper wallpaper "$MONITOR,$PICK"

    CURRENT="$PICK"
    sleep "$INTERVAL"
done
