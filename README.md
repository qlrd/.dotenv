# .dotenv

Personal dotfiles for [qlrd](https://github.com/qlrd) — editor configs and shell setup tuned for 42 school / norminette workflow.

## Structure

```
.dotenv/
├── helix/                  # Helix editor
│   ├── config.toml
│   ├── languages.toml
│   ├── themes/
│   └── scripts/
│       ├── 42header.py         # Insert/update 42 school header (F1)
│       └── norminette_wrap.py  # norminette → efm-langserver bridge
├── efm-langserver/         # efm-langserver config (norminette LSP)
│   └── config.yaml
├── vim/
│   └── vimrc               # Vim config (mirrors Helix style)
└── zsh/
    └── zshrc               # Zsh config, aliases, PATH, 42 identity
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
mkdir -p ~/.config/helix/themes
ln -sf ~/github/.dotenv/helix/config.toml ~/.config/helix/config.toml
ln -sf ~/github/.dotenv/helix/languages.toml ~/.config/helix/languages.toml
ln -sf ~/github/.dotenv/helix/themes/onedark_transparent.toml ~/.config/helix/themes/
ln -sf ~/github/.dotenv/helix/scripts ~/.config/helix/scripts
```

### 4. efm-langserver (norminette inline diagnostics)

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

### 42 Header — `F1`

Press `F1` in Helix or Vim to insert or update the 42 school header in the current file.

- First press: inserts the header at the top
- Subsequent presses: updates the `Updated` timestamp, preserves `Created`

### Norminette LSP

Norminette errors and notices appear inline in Helix via efm-langserver.
Vim uses ALE with the same norminette binary.

Quick check from the command line:

```zsh
norm yourfile.c
```

### Norminette style (C files)

| Setting | Value |
|---------|-------|
| Indentation | Tabs |
| Tab width | 4 |
| Max line length | 80 |
| Ruler | 80 |

## Dependencies

| Tool | Install |
|------|---------|
| [Helix](https://helix-editor.com) | `pacman -S helix` |
| [norminette](https://github.com/42School/norminette) | `pip install norminette` |
| [efm-langserver](https://github.com/mattn/efm-langserver) | `go install github.com/mattn/efm-langserver@latest` |
| [vim-plug](https://github.com/junegunn/vim-plug) | see link |
