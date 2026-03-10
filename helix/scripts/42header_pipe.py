#!/usr/bin/env python3
"""42 School header — stdin → stdout pipe version for Helix :pipe."""

import os
import re
import sys
from datetime import datetime

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
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        sys.stdout.write(sys.stdin.read())
        return

    filepath = sys.argv[1].strip()
    content = sys.stdin.read()
    lines = content.splitlines(keepends=True)

    has_header = (
        len(lines) >= 11
        and lines[0].rstrip("\n") == MARKER
        and lines[10].rstrip("\n") == MARKER
    )

    if has_header:
        created = None
        m = re.search(r"Created:\s+(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})", lines[7])
        if m:
            created = m.group(1)
        sys.stdout.write(build_header(filepath, created) + "".join(lines[11:]))
    else:
        sys.stdout.write(build_header(filepath) + content)


if __name__ == "__main__":
    main()
