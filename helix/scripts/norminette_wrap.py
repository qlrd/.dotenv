#!/usr/bin/env python3
"""Wrap norminette output into efm-langserver format.

Output format: filename:line:col:severity:message
  severity: E (error) | W (warning/notice)
"""

import re
import subprocess
import sys

NORMINETTE = "/home/qlrd/.piscinne/bin/norminette"
ANSI = re.compile(r"\x1b\[[0-9;]*m")
PATTERN = re.compile(
    r"^(Error|Notice): \w+\s+\(line:\s*(\d+), col:\s*(\d+)\):\s*(.+)$"
)


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    filepath = sys.argv[1]
    result = subprocess.run(
        [NORMINETTE, filepath],
        capture_output=True,
        text=True,
    )

    output = ANSI.sub("", result.stdout + result.stderr)

    for line in output.splitlines():
        m = PATTERN.match(line.strip())
        if not m:
            continue
        kind, lnum, col, msg = m.groups()
        severity = "E" if kind == "Error" else "W"
        print(f"{filepath}:{lnum}:{col}:{severity}:{msg.strip()}")

    sys.exit(result.returncode if result.returncode != 0 else 0)


if __name__ == "__main__":
    main()
