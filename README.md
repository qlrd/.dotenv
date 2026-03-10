# .dotenv

Personal dotfiles for [qlrd](https://github.com/qlrd) — editor configs and shell setup tuned for 42 school / norminette workflow.

## Structure

```
.dotenv/
├── helix/                  # Helix editor
│   ├── config.toml
│   ├── languages.toml
│   ├── themes/
│   │   └── onedark_transparent.toml
│   └── scripts/
│       ├── 42header_pipe.py    # stdin→stdout header script (shared by helix + vim)
│       ├── 42header.py         # in-place header script (legacy)
│       └── norminette_wrap.py  # norminette → efm-langserver bridge
├── efm-langserver/         # efm-langserver config (norminette LSP for Helix)
│   └── config.yaml
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

### 2. Zsh

```zsh
ln -sf ~/github/.dotenv/zsh/zshrc ~/.zshrc
```

### 3. Helix

```zsh
mkdir -p ~/.config/helix/themes ~/.cache/helix
ln -sf ~/github/.dotenv/helix/config.toml ~/.config/helix/config.toml
ln -sf ~/github/.dotenv/helix/languages.toml ~/.config/helix/languages.toml
ln -sf ~/github/.dotenv/helix/themes/onedark_transparent.toml ~/.config/helix/themes/
ln -sf ~/github/.dotenv/helix/scripts ~/.config/helix/scripts
```

### 4. efm-langserver (norminette inline diagnostics for Helix)

Install:

```zsh
go install github.com/mattn/efm-langserver@latest
```

Link config:

```zsh
mkdir -p ~/.config/efm-langserver
ln -sf ~/github/.dotenv/efm-langserver/config.yaml ~/.config/efm-langserver/config.yaml
```

### 5. Vim

```zsh
ln -sf ~/github/.dotenv/vim/vimrc ~/.vimrc
```

Install [vim-plug](https://github.com/junegunn/vim-plug), then run `:PlugInstall` in vim to get ALE.

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

## Dependencies

| Tool | Install |
|------|---------|
| [Helix](https://helix-editor.com) | `pacman -S helix` |
| [norminette](https://github.com/42School/norminette) | `pip install norminette` |
| [efm-langserver](https://github.com/mattn/efm-langserver) | `go install github.com/mattn/efm-langserver@latest` |
| [vim-plug](https://github.com/junegunn/vim-plug) | see link |
