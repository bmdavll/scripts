#!/usr/bin/env python3
import sys

def escape(char):
    c = ord(char)
    if c <= 0xff:
        return r'\x%02x' % c
    else:
        if c <= 0xffff:
            return r'\u%04x' % c
        else:
            return r'\U%08x' % c

def convert(stream):
    for line in stream:
        print(''.join(map(escape, line)), end='')

errors = 0

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
    sys.exit(1)
