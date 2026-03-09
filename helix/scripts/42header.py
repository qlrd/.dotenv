#!/usr/bin/env python3
"""42 School header — insert or update in-place.

Usage: 42header.py <filepath>

Env vars:
  FT_LOGIN  — 42 login (default: qlrd)
  FT_EMAIL  — 42 email (default: qlrd@student.42.fr)
"""

import os
import re
import sys
from datetime import datetime

W = 80
LOGIN = os.environ.get("FT_LOGIN", "qlrd")
EMAIL = os.environ.get("FT_EMAIL", "qlrd@student.42.fr")
MARKER = "/* " + "*" * 74 + " */"


def build_header(filepath, created=None):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    if created is None:
        created = now
    fn = os.path.basename(filepath)
    by = f"{LOGIN} <{EMAIL}>"
    return "\n".join([
        "/* " + "*" * 74 + " */",
        "/*" + " " * 76 + "*/",
        "/*" + " " * 56 + ":::      ::::::::   */",
        f"/*   {fn:<51}:+:      :+:    :+:   */",
        "/*" + " " * 52 + "+:+ +:+         +:+     */",
        f"/*   By: {by:<43}+#+  +:+       +#+        */",
        "/*" + " " * 48 + "+#+#+#+#+#+   +#+           */",
        f"/*   Created: {created} by {LOGIN:<18}#+#    #+#             */",
        f"/*   Updated: {now} by {LOGIN:<17}###   ########.fr       */",
        "/*" + " " * 76 + "*/",
        "/* " + "*" * 74 + " */",
    ]) + "\n"


def main():
    if len(sys.argv) < 2:
        print("Usage: 42header.py <filepath>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        with open(filepath, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = ""

    lines = content.splitlines(keepends=True)

    # Detect existing header: starts and ends with MARKER
    has_header = (
        len(lines) >= 11
        and lines[0].rstrip("\n") == MARKER
        and lines[10].rstrip("\n") == MARKER
    )

    if has_header:
        # Extract original Created timestamp
        created = None
        m = re.search(r"Created:\s+(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})", lines[7])
        if m:
            created = m.group(1)
        new_header = build_header(filepath, created)
        new_content = new_header + "".join(lines[11:])
    else:
        new_content = build_header(filepath) + content

    with open(filepath, "w") as f:
        f.write(new_content)


if __name__ == "__main__":
    main()
