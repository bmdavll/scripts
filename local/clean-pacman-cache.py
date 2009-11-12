#!/usr/bin/python3

import os, re, sys
from glob import glob
from collections import defaultdict

re_suffix = re.compile(r'-[^-]+-[\d.]+(-i686)?\.pkg\.tar\.gz$')

count = defaultdict(lambda: 0)

os.chdir('/var/cache/pacman/pkg')

for pkg in glob('*'):
    count[re_suffix.sub('', pkg)] += 1

keep = 3

if len(sys.argv) == 2 and re.match(r'^[1-9][0-9]*$', sys.argv[1]):
    keep = int(sys.argv[1])

try:
    for key in count:
        if count[key] > keep:
            if key.startswith('kernel') and count[key] <= keep+2:
                continue
            extra = filter( lambda s: re_suffix.sub('', s) == key,
                            glob(key + '-*') )
            for file in sorted(extra)[ : -keep]:
                os.remove(file)
                print(file)
except OSError as e:
    print(e.strerror, e.filename, sep=': ', file=sys.stderr)
