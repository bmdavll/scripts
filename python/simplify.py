#!/usr/bin/env python3

import sys, os, re

__table__ = 'zhtable.txt'

__prog__ = os.path.basename(sys.argv[0])
__usage__ = '''%(__prog__)s
Convert text from traditional Chinese to simplified Chinese
David Liang (bmdavll@gmail.com)

Usage: %(__prog__)s [traditional.txt]... > simplified.txt

If no command-line arguments are specified, the standard input will be used.
The character mappings are read from %(__table__)s, which must be in the same
directory as this script.\
''' % globals()

for arg in sys.argv[1:]:
    if re.match(r'(-h|--help$|-\?|--usage$)', arg):
        print(usage)
        sys.exit(0)


def init(basename):
    global map
    try:
        with open(os.path.join(sys.path[0], basename)) as file:
            lnum = 0
            for line in file:
                lnum += 1
                line = re.sub(r'(^|\s)#.*', '', line).strip()
                if not line:
                    continue
                assert len(line) == 3 and line[1] == '='
                map[ ord(line[2]) ] = ord(line[0])

    except AssertionError as e:
        print('%s: %d: Bad line (each line should be in the form of "国=國")'
               % (basename, lnum), file=sys.stderr)
        sys.exit(1)


def convert(stream):
    print(stream.read()[:-1].translate(map))


map = {}
errors = 0

try:
    init(__table__)
except IOError as e:
    print(e.filename+':', e.strerror, file=sys.stderr)
    sys.exit(2)

if len(sys.argv) == 1:
    try:
        convert(sys.stdin)
    except IOError as e:
        print(e.strerror, file=sys.stderr)
        errors += 1
else:
    for file in sys.argv[1:]:
        try:
            with open(file) as input:
                convert(input)
        except IOError as e:
            print(e.filename+':', e.strerror, file=sys.stderr)
            errors += 1

if errors > 0:
    sys.exit(2)
