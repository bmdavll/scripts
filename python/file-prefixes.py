#!/usr/bin/env python3

import sys, os

lines = set()
prefixes = set()

try:

    for line in sys.stdin:
        lines.add(line.rstrip('\n'))

    if '' in lines:
        lines.remove('')

    def check(line):
        global prefixes

        for prefix in prefixes:
            if line.startswith(prefix.rstrip(os.sep) + os.sep):
                return

        prefixes.add(line)

    for line in sorted(lines):
        check(line)

    for prefix in prefixes:
        print(prefix)

except KeyboardInterrupt:
    sys.exit(1)
