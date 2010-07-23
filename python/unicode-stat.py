#!/usr/bin/env python3

import sys, re
from unicodedata import name


def errprint(*args, sep=' ', end='\n', file=sys.stderr):
    print(*args, sep=sep, end=end, file=file)


def codepoint(char):
    h = hex(ord(char)).replace('0x', '', 1).upper()

    if len(h) > 8:
        h = ''
    elif len(h) > 4:
        h = ('000' + h)[-8:]
    elif h:
        h = ('000' + h)[-4:]

    if h:
        return 'U' + h
    else:
        return ''


def emit(chars):
    global errors

    print(chars, end='')
    for c in chars:
        u = codepoint(c)
        if u:
            try:
                desc = ' # '+name(c)
            except ValueError:
                desc = ''
                errors += 1

            print('\t%s%s' % (u, desc), end='')
        else:
            errprint(c+':', 'Code point not found')
            errors += 1
    print()


def read(file):
    for line in file:
        emit(line.strip())


# input file format:
# æ
# ɛ
# …

errors = 0

if len(sys.argv) == 1:
    read(sys.stdin)

else:
    for file in sys.argv[1:]:
        try:
            with open(file) as f:
                read(f)
        except IOError as e:
            errprint(e.filename+':', e.strerror)
            errors += 1

sys.exit(errors)
