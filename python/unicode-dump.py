#!/usr/bin/env python3

from unicodedata import name

for i in range(0x1, 0x10000):
    c = chr(i)
    try:
        print(c, 'U+%04X' % i, '# '+name(c))
    except ValueError:
        pass
