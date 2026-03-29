#!/usr/bin/env python3
"""
backup.py — Home directory backup to .home.tar.xz
Location: ~/github/.dotenv/backup.py

Usage:
    python3 backup.py [--output PATH] [--dry-run] [--list-excluded] [--verbose]

Restore:
    tar -xf .home.tar.xz -C /home
"""

import argparse
import fnmatch
import os
import sys
import tarfile


# ---------------------------------------------------------------------------
# Exclusion rules — all constants live here, nowhere else
# ---------------------------------------------------------------------------

# Top-level directory names under $HOME to skip entirely
TOP_LEVEL_DIRS: frozenset[str] = frozenset({
    # Git repos (safe on GitHub)
    "github",
    "42",
    "mini-moulinette",
    # Reinstallable toolchains
    ".oh-my-zsh",
    ".cargo",
    ".rustup",
    "go",
    # Large application directories
    ".opencode",
    ".ollama",
    ".vscode-oss",
    # Non-config user directories
    "Downloads",
    "Desktop",
    "Picutres",          # typo preserved from actual dir name
    # Browser / runtime junk
    ".steam",
    ".mozilla",
    ".pki",
})

# Sub-paths relative to $HOME to skip (exact or prefix match).
# Handles both multi-level paths (.config/discord) and large regular files (.veracrypt).
SUBPATH_EXCLUDES: tuple[str, ...] = (
    # Python installations — keep shims/config, skip heavy runtimes
    ".pyenv/versions",
    # Wallpaper binaries
    ".config/hypr/walls",
    # Browser / Electron caches
    ".config/discord",
    ".config/librewolf",
    ".config/chromium",
    ".config/BraveSoftware",
    ".config/Signal",
    ".config/Electron",
    ".config/VSCodium",
    # ~/.local heavy hitters
    ".local/share/Steam",
    ".local/share/discord",
    ".local/share/TelegramDesktop",
    ".local/share/baloo",
    ".local/share/gvfs-metadata",
    ".local/share/flatpak",
    # ~/.local reinstallable subtrees
    ".local/state",
    ".local/bin",
    ".local/opt",
    ".local/lib",
    ".local/share/man",
    # Claude Code runtime data (keep settings + memory)
    ".claude/projects",
    ".claude/debug",
    ".claude/cache",
    ".claude/paste-cache",
    ".claude/file-history",
    ".claude/telemetry",
    ".claude/shell-snapshots",
    # VeraCrypt volume — 15 GB, backed up separately
    ".veracrypt",
)

# fnmatch patterns matched against the bare filename
NAME_PATTERNS: tuple[str, ...] = (
    ".zcompdump*",
    ".home.tar.xz",
    ".home.tar.xz.gpg",
    "latest.tar.gz",
    ".VeraCrypt-lock-*",
)

PROGRESS_INTERVAL = 500
DEFAULT_OUTPUT = os.path.join(os.path.expanduser("~"), ".home.tar.xz")


# ---------------------------------------------------------------------------
# Core exclusion logic
# ---------------------------------------------------------------------------

def should_exclude(rel: str, name: str) -> bool:
    """
    Pure predicate — no I/O, no side-effects.

    Parameters
    ----------
    rel  : path relative to $HOME using os.sep  (e.g. '.config/hypr/walls')
    name : bare filename component              (e.g. 'walls')
    """
    # 1. Name patterns (cheapest check first)
    for pattern in NAME_PATTERNS:
        if fnmatch.fnmatch(name, pattern):
            return True

    # 2. Sub-path: exact match or any descendant
    for sp in SUBPATH_EXCLUDES:
        if rel == sp or rel.startswith(sp + os.sep):
            return True

    return False


# ---------------------------------------------------------------------------
# Filesystem walker
# ---------------------------------------------------------------------------

def walk_home(
    home: str,
    verbose: bool,
    output_path: str,
) -> tuple[list[tuple[str, str]], int]:
    """
    Walk $HOME with topdown pruning via dirnames[:].
    Returns (entries, total_uncompressed_bytes).

    entries is a list of (abs_path, arcname) where arcname is relative to
    the parent of $HOME, e.g. 'qlrd/.zshrc'.  Restore with:
        tar -xf .home.tar.xz -C /home

    Broken symlinks are skipped silently.
    Permission errors are skipped with a warning to stderr.
    """
    home_basename = os.path.basename(home)
    output_abs = os.path.realpath(output_path)

    entries: list[tuple[str, str]] = []
    total_bytes = 0

    for dirpath, dirnames, filenames in os.walk(home, topdown=True, followlinks=False):
        rel_dir = os.path.relpath(dirpath, home)  # '.' at root

        # --- Prune directories in-place ---
        keep: list[str] = []
        for d in dirnames:
            if rel_dir == ".":
                if d in TOP_LEVEL_DIRS:
                    continue
                child_rel = d
            else:
                child_rel = os.path.join(rel_dir, d)

            if should_exclude(child_rel, d):
                continue

            keep.append(d)
        dirnames[:] = keep

        # --- Directory entry itself (skip HOME root) ---
        if rel_dir != ".":
            arcname = os.path.join(home_basename, rel_dir)
            entries.append((dirpath, arcname))

        # --- Files and symlinks ---
        for filename in filenames:
            abs_path = os.path.join(dirpath, filename)
            child_rel = filename if rel_dir == "." else os.path.join(rel_dir, filename)

            # Skip the output archive itself
            try:
                if os.path.realpath(abs_path) == output_abs:
                    continue
            except OSError:
                pass

            if should_exclude(child_rel, filename):
                continue

            # Skip broken symlinks silently
            if os.path.islink(abs_path) and not os.path.exists(abs_path):
                continue

            try:
                st = os.lstat(abs_path)
            except PermissionError:
                print(f"WARNING: permission denied, skipping: {abs_path}", file=sys.stderr)
                continue
            except OSError as exc:
                print(f"WARNING: cannot stat, skipping: {abs_path} ({exc})", file=sys.stderr)
                continue

            arcname = os.path.join(home_basename, child_rel)
            entries.append((abs_path, arcname))
            total_bytes += st.st_size

            if verbose:
                print(arcname, file=sys.stderr)

    return entries, total_bytes


# ---------------------------------------------------------------------------
# Archive writer
# ---------------------------------------------------------------------------

def create_archive(entries: list[tuple[str, str]], output_path: str) -> int:
    """
    Write entries to a .tar.xz archive.
    Returns the number of files/symlinks added (directories not counted).
    Prints progress to stderr every PROGRESS_INTERVAL files.
    """
    file_count = 0

    with tarfile.open(output_path, "w:xz", dereference=False) as tar:
        for abs_path, arcname in entries:
            try:
                tar.add(abs_path, arcname=arcname, recursive=False)
            except PermissionError:
                print(f"WARNING: permission denied archiving: {abs_path}", file=sys.stderr)
                continue
            except OSError as exc:
                print(f"WARNING: OS error archiving: {abs_path} ({exc})", file=sys.stderr)
                continue

            if os.path.isfile(abs_path) or os.path.islink(abs_path):
                file_count += 1
                if file_count % PROGRESS_INTERVAL == 0:
                    print(f"  ... {file_count} files added", file=sys.stderr)

    return file_count


# ---------------------------------------------------------------------------
# CLI helpers
# ---------------------------------------------------------------------------

def cmd_list_excluded() -> None:
    print("Top-level directories excluded from $HOME:")
    for d in sorted(TOP_LEVEL_DIRS):
        print(f"  $HOME/{d}/")

    print("\nSub-paths excluded (prefix match from $HOME):")
    for sp in SUBPATH_EXCLUDES:
        print(f"  $HOME/{sp}")

    print("\nFilename patterns excluded (fnmatch):")
    for p in NAME_PATTERNS:
        print(f"  {p}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="backup.py",
        description="Create a .home.tar.xz backup of $HOME with surgical exclusions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 backup.py\n"
            "  python3 backup.py --dry-run\n"
            "  python3 backup.py --output /mnt/usb/.home.tar.xz --verbose\n"
            "  python3 backup.py --list-excluded\n\n"
            "Restore:\n"
            "  tar -xf .home.tar.xz -C /home"
        ),
    )
    parser.add_argument(
        "--output", "-o",
        default=DEFAULT_OUTPUT,
        metavar="PATH",
        help=f"output archive path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="list files that would be archived; do not write anything",
    )
    parser.add_argument(
        "--list-excluded",
        action="store_true",
        help="print all exclusion rules and exit",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="print each path as it is added (to stderr)",
    )
    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    args = build_parser().parse_args()

    if args.list_excluded:
        cmd_list_excluded()
        return 0

    home = os.path.expanduser("~")
    if not os.path.isdir(home):
        print(f"ERROR: home directory not found: {home}", file=sys.stderr)
        return 1

    output_path = os.path.expanduser(args.output)

    print(f"Source:  {home}", file=sys.stderr)
    print(f"Output:  {output_path}", file=sys.stderr)
    if args.dry_run:
        print("Mode:    dry-run", file=sys.stderr)
    print(file=sys.stderr)

    entries, total_bytes = walk_home(home, args.verbose, output_path)

    if args.dry_run:
        file_count = 0
        for abs_path, arcname in entries:
            if os.path.isfile(abs_path) or os.path.islink(abs_path):
                print(arcname)
                file_count += 1
        size_mb = total_bytes / (1024 * 1024)
        print(f"\nDry-run: {file_count} files, {size_mb:.1f} MB uncompressed", file=sys.stderr)
        return 0

    print("Archiving...", file=sys.stderr)
    try:
        file_count = create_archive(entries, output_path)
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    uncompressed_mb = total_bytes / (1024 * 1024)
    try:
        compressed_mb = os.path.getsize(output_path) / (1024 * 1024)
    except OSError:
        compressed_mb = 0.0

    print(
        f"\nDone: {file_count} files, "
        f"{uncompressed_mb:.1f} MB uncompressed → {compressed_mb:.1f} MB compressed",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
