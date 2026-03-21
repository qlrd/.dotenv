#!/usr/bin/env bash
# Hyprland keybindings cheatsheet — lazygit-style overlay
# q / ESC to close   ↑↓ / j·k to scroll

B=$'\033[1m'       # Bold yellow (alacritty fg is already yellow)
W=$'\033[1;97m'    # Bold bright white — descriptions
D=$'\033[2m'       # Dim — decorative borders
R=$'\033[0m'       # Reset

# Section header
section() {
    local title="$1"
    local pad
    pad=$(printf '─%.0s' $(seq 1 $((56 - ${#title}))))
    printf "\n${B}  ── %s %s${R}\n\n" "$title" "${D}${pad}${R}"
}

# Keybind row: bold-yellow key, white description
bind() {
    printf "  ${B}%-34s${R}  ${W}%s${R}\n" "$1" "$2"
}

# ── Output ────────────────────────────────────────────────────────────
{
    printf "${B}"
    printf "  ╔══════════════════════════════════════════════════════════════╗\n"
    printf "  ║       ⌨   HYPRLAND  KEYBINDINGS  CHEATSHEET   ⌨           ║\n"
    printf "  ║                   q / ESC  ·  close   ↑↓ · j·k  ·  scroll ║\n"
    printf "  ╚══════════════════════════════════════════════════════════════╝\n"
    printf "${R}"

    section "WINDOWS"
    bind "SUPER + Return"            "Open terminal"
    bind "SUPER + Shift + Return"    "Open floating terminal"
    bind "SUPER + Q  /  Alt + F4"   "Close window"
    bind "SUPER + F11"               "Fullscreen"
    bind "SUPER + S"                 "Toggle floating"
    bind "SUPER + P"                 "Pseudo-tile (dwindle)"
    bind "SUPER + J"                 "Toggle split"

    section "NAVIGATION"
    bind "SUPER + ← ↑ → ↓"          "Move focus"
    bind "Alt + Tab"                  "Cycle next window"
    bind "SUPER + Tab"                "Swap with next window"
    bind "SUPER + [1-9]"              "Switch to workspace"
    bind "SUPER + Mouse Scroll"       "Scroll through workspaces"

    section "MOVE & RESIZE"
    bind "SUPER + Shift + [1-9]"      "Move window to workspace"
    bind "SUPER + Shift + ← ↑ → ↓"   "Resize window"
    bind "SUPER + LMB drag"           "Move window"
    bind "SUPER + RMB drag"           "Resize window"

    section "APPS & ROFI"
    bind "SUPER + Space"              "App launcher"
    bind "SUPER + R"                  "Run command"
    bind "SUPER + Shift + Space"      "Emoji picker"
    bind "SUPER + E"                  "Files (Dolphin)"
    bind "SUPER + F"                  "Browser"
    bind "SUPER + Shift + F"          "Browser (private window)"
    bind "SUPER + T"                  "Telegram"
    bind "SUPER + L"                  "Lock screen"
    bind "SUPER + X"                  "Power menu"

    section "CLIPBOARD"
    bind "SUPER + C"                  "Copy"
    bind "SUPER + V"                  "Paste"
    bind "SUPER + Shift + V"          "Clipboard history"

    section "SCREENSHOT"
    bind "Print"                      "Fullscreen screenshot → clipboard + file"
    bind "Shift + Print"              "Region screenshot → clipboard + file"

    section "SYSTEM"
    bind "SUPER + Shift + R"          "Reload Hyprland"
    bind "SUPER + Shift + Alt + P"    "Shutdown"
    bind "SUPER + Shift + Alt + R"    "Reboot"
    bind "SUPER + Shift + Alt + L"    "Logout"
    bind "SUPER + Shift + Alt + S"    "Turn screen off"
    bind "SUPER + Shift + S"          "Turn screen on"

    section "MEDIA"
    bind "Brightness Up / Down"       "Screen brightness ±5%"
    bind "Volume Up / Down"           "Audio volume ±5%"
    bind "Mute"                       "Toggle mute"
    bind "Play / Next / Prev / Stop"  "Media playback controls"

    printf "\n${D}  ──────────────────────────────────────────────────────────────${R}\n\n"

} | less -R -K -P "  [q/ESC] close   [↑↓ · j·k] scroll   [/] search"
