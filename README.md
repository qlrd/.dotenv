# .dotenv

Personal dotfiles for [qlrd](https://github.com/qlrd) — editor, shell, terminal, and Hyprland desktop configs.

## Structure

```
.dotenv/
├── alacritty/              # Terminal emulator (Catppuccin Mocha, FiraCode Nerd Font)
│   ├── alacritty.toml
│   └── helper.toml         # Keybindings helper overlay (transparent, yellow text)
├── efm-langserver/         # efm-langserver config (norminette LSP for Helix)
│   └── config.yaml
├── gitconfig               # Git identity, GPG signing, gh credential helper
├── helix/                  # Helix editor
│   ├── config.toml
│   ├── languages.toml
│   ├── themes/
│   │   └── onedark_transparent.toml
│   └── scripts/
│       ├── 42header_pipe.py    # stdin→stdout header script (shared by helix + vim)
│       ├── 42header.py         # in-place header script (legacy)
│       └── norminette_wrap.py  # norminette → efm-langserver bridge
├── hypr/                   # Hyprland WM
│   ├── hyprland.conf       # Main config: monitor, input, keybinds, rules
│   ├── hypridle.conf       # Idle timeouts: dim → lock → dpms off
│   ├── hyprlock.conf       # Lock screen: Catppuccin, clock, blur
│   ├── hyprpaper.conf      # Wallpaper per monitor
│   └── scripts/
│       ├── random-wallpaper.sh   # Rotate wallpapers from walls/ every hour
│       ├── nogaps.sh             # Auto gaps: 0 gaps when single window
│       ├── keybinds-helper.sh    # Alacritty overlay showing keybinds
│       ├── nm-applet-no-systray.sh
│       └── reload.sh             # Reload waybar + hyprpaper + hyprland
├── rofi/                   # App launcher menus
│   ├── style-1.rasi
│   ├── bluetooth/
│   ├── clipboard/
│   ├── colors/
│   ├── emoji/
│   ├── filebrowser/
│   ├── launchers/
│   ├── powermenu/
│   ├── run/
│   ├── shared/
│   ├── snippet/
│   ├── wifi/
│   └── window/
├── ssh/
│   └── config              # SSH host config (Yubikey for github.com)
├── tmux/
│   └── tmux.conf           # Catppuccin status bar, sensible defaults
├── vim/
│   └── vimrc               # Vim config — same F1 and norminette features as Helix
└── zsh/
    └── zshrc               # Zsh config: aliases, PATH, 42 identity, tab width
```

## Setup

### 1. Identity

Set your 42 login and email. The header scripts and zsh config use these:

```zsh
export FT_LOGIN="yourlogin"
export FT_EMAIL="yourlogin@student.42.fr"
```

Add them to `~/.zshrc.local` on shared machines to avoid committing personal info.

### 2. Git

```zsh
cp ~/github/.dotenv/gitconfig ~/.gitconfig
# then edit [user] fields and signingkey
```

### 3. SSH

```zsh
cp ~/github/.dotenv/ssh/config ~/.ssh/config
chmod 700 ~/.ssh && chmod 600 ~/.ssh/config
```

### 4. Zsh

```zsh
ln -sf ~/github/.dotenv/zsh/zshrc ~/.zshrc
```

### 5. Helix

```zsh
mkdir -p ~/.config/helix/themes ~/.cache/helix
ln -sf ~/github/.dotenv/helix/config.toml ~/.config/helix/config.toml
ln -sf ~/github/.dotenv/helix/languages.toml ~/.config/helix/languages.toml
ln -sf ~/github/.dotenv/helix/themes/onedark_transparent.toml ~/.config/helix/themes/
ln -sf ~/github/.dotenv/helix/scripts ~/.config/helix/scripts
```

### 6. efm-langserver (norminette inline diagnostics for Helix)

Install:

```zsh
go install github.com/mattn/efm-langserver@latest
```

Link config:

```zsh
mkdir -p ~/.config/efm-langserver
ln -sf ~/github/.dotenv/efm-langserver/config.yaml ~/.config/efm-langserver/config.yaml
```

### 7. Vim

```zsh
ln -sf ~/github/.dotenv/vim/vimrc ~/.vimrc
```

Install [vim-plug](https://github.com/junegunn/vim-plug), then run `:PlugInstall` in vim to get ALE.

### 8. Alacritty

```zsh
mkdir -p ~/.config/alacritty
ln -sf ~/github/.dotenv/alacritty/alacritty.toml ~/.config/alacritty/alacritty.toml
ln -sf ~/github/.dotenv/alacritty/helper.toml ~/.config/alacritty/helper.toml
```

### 9. Tmux

```zsh
mkdir -p ~/.config/tmux
ln -sf ~/github/.dotenv/tmux/tmux.conf ~/.config/tmux/tmux.conf
```

### 10. Hyprland

```zsh
mkdir -p ~/.config/hypr/scripts ~/.config/hypr/walls
ln -sf ~/github/.dotenv/hypr/hyprland.conf ~/.config/hypr/hyprland.conf
ln -sf ~/github/.dotenv/hypr/hypridle.conf ~/.config/hypr/hypridle.conf
ln -sf ~/github/.dotenv/hypr/hyprlock.conf ~/.config/hypr/hyprlock.conf
ln -sf ~/github/.dotenv/hypr/hyprpaper.conf ~/.config/hypr/hyprpaper.conf
ln -sf ~/github/.dotenv/hypr/scripts/random-wallpaper.sh ~/.config/hypr/scripts/
ln -sf ~/github/.dotenv/hypr/scripts/nogaps.sh ~/.config/hypr/scripts/
ln -sf ~/github/.dotenv/hypr/scripts/keybinds-helper.sh ~/.config/hypr/scripts/
ln -sf ~/github/.dotenv/hypr/scripts/nm-applet-no-systray.sh ~/.config/hypr/scripts/
ln -sf ~/github/.dotenv/hypr/scripts/reload.sh ~/.config/hypr/scripts/
# add wallpapers to ~/.config/hypr/walls/
```

### 11. Waybar

```zsh
mkdir -p ~/.config/waybar
ln -sf ~/github/.dotenv/waybar/config.jsonc ~/.config/waybar/config.jsonc
ln -sf ~/github/.dotenv/waybar/style.css ~/.config/waybar/style.css
```

### 12. Rofi

```zsh
ln -sf ~/github/.dotenv/rofi ~/.config/rofi
```

## Features

### Zsh

| Feature | Detail |
|---------|--------|
| 42 identity | `$FT_LOGIN` / `$FT_EMAIL` exported for header scripts |
| PATH | Prepends `~/.local/bin`, `~/bin`, `~/go/bin` if they exist |
| Editor | `$EDITOR=vim`, `v`/`vi` → vim, `hx` → helix |
| Tab width | `tabs -4` so terminal tab stops match norminette's count |
| Aliases | `norm` → norminette, `gs` → git status, `gd` → git diff, `ll`, `la` |
| Local overrides | Sources `~/.zshrc.local` if present (for machine-specific settings) |

### Helix

| Feature | Detail |
|---------|--------|
| Theme | `onedark_transparent` — onedark with transparent background |
| Indentation | Tabs, width 4, `smart-tab` disabled, `indent-heuristic = simple` |
| Ruler | 80 columns |
| Soft wrap | Enabled, max-indent-retain 80 |
| Indent guides | `┊` character, skip first level |
| Gutters | Line numbers, diff, diagnostics, spacer |
| LSP | efm-langserver wired for C (norminette inline diagnostics) |
| Auto-save | Enabled |
| `F1` | Insert / update 42 school header (preserves `Created` timestamp) |
| `C-g` | Open lazygit at the repo root of the current file |
| Cursor shapes | Normal: hidden, Insert: bar, Select: block |
| Status line | Mode labels: `LOCKED` / `WORKING` / `VISUAL SEL` |

### Vim

| Feature | Detail |
|---------|--------|
| Indentation | Tabs, width 4, `noexpandtab` |
| Ruler | `colorcolumn=80`, `textwidth=80` |
| `F1` | Insert / update 42 school header via `%!` pipe (same script as Helix) |
| `:Norm` | Run norminette on the current file and show output |
| ALE | Inline norminette diagnostics on save (requires vim-plug + `:PlugInstall`) |
| Plugins | `dense-analysis/ale`, `preservim/nerdcommenter` |

### 42 Header — `F1`

Press `F1` in Helix or Vim to insert or update the 42 school header.

- First press: inserts the header at the top
- Subsequent presses: updates the `Updated` timestamp, preserves `Created`
- Uses `$FT_LOGIN` / `$FT_EMAIL` (falls back to values set in zshrc)
- Implemented as a stdin→stdout pipe (`42header_pipe.py`) — no temp files

### Norminette style (C files)

| Setting | Value |
|---------|-------|
| Indentation | Tabs |
| Tab width | 4 |
| Max line length | 80 |

### Alacritty

| Feature | Detail |
|---------|--------|
| Theme | Catppuccin Mocha |
| Font | FiraCode Nerd Font, size 12 |
| Opacity | 0.69 with `decorations = none` |
| Padding | 20px x/y |
| `helper.toml` | Alternate color profile for keybinds overlay (0.15 opacity) |

### Tmux

| Feature | Detail |
|---------|--------|
| Theme | Catppuccin Mocha (manual, no plugin required) |
| Base index | 1 (windows and panes) |
| Mouse | Enabled |
| Status | Session name, window list, hostname, time, date |
| History | 10,000 lines |
| RGB | True color + extended keys |

### Hyprland

| Feature | Detail |
|---------|--------|
| Monitor | Auto preferred, auto position |
| Input | Brazilian ABNT2 + Corne keyboard in US intl |
| Idle | Dim at 2.5 min → lock at 5 min → DPMS off at 5.5 min |
| Lock | hyprlock with Catppuccin, clock, blurred bg |
| Wallpaper | Random rotation from `walls/` every hour via hyprpaper |
| Gaps | Auto: 0 gaps when single window, 5/10 with multiple |
| Startup | alacritty (ws1), librewolf (ws2), veracrypt + keepassxc (ws3) |

## Dependencies

| Tool | Install |
|------|---------|
| [Helix](https://helix-editor.com) | `pacman -S helix` |
| [norminette](https://github.com/42School/norminette) | `pip install norminette` |
| [efm-langserver](https://github.com/mattn/efm-langserver) | `go install github.com/mattn/efm-langserver@latest` |
| [vim-plug](https://github.com/junegunn/vim-plug) | see link |
| [Alacritty](https://alacritty.org) | `pacman -S alacritty` |
| [Tmux](https://github.com/tmux/tmux) | `pacman -S tmux` |
| [Hyprland](https://hyprland.org) | `pacman -S hyprland` |
| [hyprpaper](https://github.com/hyprwm/hyprpaper) | `pacman -S hyprpaper` |
| [hyprlock](https://github.com/hyprwm/hyprlock) | `pacman -S hyprlock` |
| [hypridle](https://github.com/hyprwm/hypridle) | `pacman -S hypridle` |
| [waybar](https://github.com/Alexays/Waybar) | `pacman -S waybar` |
| [rofi-wayland](https://github.com/lbonn/rofi) | `pacman -S rofi-wayland` |
| [FiraCode Nerd Font](https://www.nerdfonts.com) | `pacman -S ttf-firacode-nerd` |
