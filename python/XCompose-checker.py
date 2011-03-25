#!/usr/bin/env python3

import sys, re
from unicodedata import name


def stdprint(*args, sep=' ', end='\n', file=sys.stderr):
    if not ucode:
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


def emit(line):
    if not ucode:
        return

    m = re.match(r'^((?:\s*<\w+>)+\s*:\s*)"(.+)"(\s*\w*\s*)(.*)', line)
    if not m:
        print(line, end='')
        return

    pre = m.group(1)
    str = m.group(2)
    aft = m.group(4)

    u = codepoint(str[0])
    if u:
        try:
            desc = ' # '+name(str[0])
        except ValueError:
            desc = (' '+aft if aft else '')

        print( '%s"%s"\t%s%s' %
               (pre, str, u, desc) )
    else:
        print(line, end='')


def check(file):
    lc = 0
    errors = 0
    bindings = {}

    stdprint("Checking for duplicates ...")

    for line in file:
        emit(line)
        lc += 1

        spec = line.strip()
        if not spec or spec.startswith("#"):
            continue

        startpos = 0
        key_seq = ''

        while True:
            m = re.match(r'\s*<(\w+)>', spec[startpos:])
            if not m:
                break
            key = m.group(1)
            key_seq += (' ' if key_seq else '') + key
            startpos += m.end()

        if startpos == 0:
            continue

        m = re.match(r'\s*:\s*"(.+)"', spec[startpos:])
        if not m:
            stdprint("Char not found on line", lc)
            errors += 1
            continue
        else:
            char = m.group(1)

        if key_seq in bindings:
            if char != bindings[key_seq]:
                stdprint( "Exact conflict found: %s: ( %s ) [%s][%s]" %
                          (lc, key_seq, bindings[key_seq], char) )
            else:
                stdprint( "Redundant definition: %s: ( %s ) [%s]" %
                          (lc, key_seq, char) )
            errors += 1
        else:
            bindings[key_seq] = char

    stdprint("\nChecking prefixes ...")

    for key_seq in bindings:
        pre = ''
        for key in key_seq.split(' ')[:-1]: # Last one will always match
            pre += (' ' if pre else '') + key
            if pre in bindings:
                stdprint( "Prefix conflict found: ( %s ) [%s]\n"
                          "                       ( %s ) [%s]" %
                          (pre, bindings[pre], key_seq, bindings[key_seq]) )
                errors += 1

    if errors == 0:
        stdprint("\nNo errors")
    else:
        stdprint("\n" + str(errors) + " error" + ("s" if errors > 1 else ""))
    return errors


code = 0
args = False
ucode = False

sep = ''
for file in sys.argv[1:]:
    if file == '-u':
        ucode = True
        continue
    try:
        args = True
        with open(file) as f:
            stdprint(sep + file)
            code += check(f)
    except IOError as e:
        stdprint(sep + e.filename+':', e.strerror)
    finally:
        sep = '\n'

if not args:
    code += check(sys.stdin)

sys.exit(code)
