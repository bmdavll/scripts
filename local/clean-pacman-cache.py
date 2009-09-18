#!/usr/bin/python3

import os, re, sys
from glob import glob
from collections import defaultdict

re_suffix = re.compile(r'-[^-]+-[\d.]+(-i686)?\.pkg\.tar\.gz$')

count = defaultdict(lambda: 0)

os.chdir('/var/cache/pacman/pkg')

for pkg in glob('*'):
    count[re_suffix.sub('', pkg)] += 1

keep = 2

try:
    for key in count:
        if count[key] > keep:
            extra = filter( lambda s: re_suffix.sub('', s) == key,
                            glob(key + '-*') )
            for file in sorted(extra)[ : -keep]:
                os.remove(file)
                print(file)
except OSError as e:
    print(e.strerror, e.filename, sep=': ', file=sys.stderr)
