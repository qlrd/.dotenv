#!/bin/bash
# Reads the selected line (function signature) from stdin.
# Extracts the function name and outputs a docblock + original line.

line=$(cat)

funcname=$(printf '%s' "$line" | grep -oP '\b[a-zA-Z_]\w*(?=\s*\()' | head -1)
if [[ -z "$funcname" ]]; then
    funcname="<function_name>"
fi

printf '/*\n'
printf ' * %s\n' "$funcname"
printf ' *\n'
printf ' * ## About\n'
printf ' *\n'
printf ' * ## Example\n'
printf ' *\n'
printf ' */\n'
printf '%s\n' "$line"
