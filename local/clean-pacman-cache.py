#!/usr/bin/python3

import os, re, sys
from glob import glob
from collections import defaultdict
from subprocess import Popen, PIPE

re_suffix = re.compile(r'-[^-]+-[^-]+(-(?:i686|x86_64|any))?\.pkg\.tar\.\w+$')

keep = 3

if len(sys.argv) == 2 and re.match(r'^[1-9][0-9]*$', sys.argv[1]):
    keep = int(sys.argv[1])

packages = defaultdict(lambda:[])

try:
    output = Popen(['pacman', '-Qq'], stdout=PIPE).communicate()[0]
    installed = set(output.decode().split())

    os.chdir('/var/cache/pacman/pkg')

    files = glob('*')
    files.sort()

    for file in files:
        packages[ re_suffix.sub('', file) ].append(file)

    for pkg in packages:

        if pkg not in installed:
            for file in packages[pkg]:
                os.remove(file)
                print(file, '[not installed]')

        elif pkg.startswith('kernel'):
            if len(packages[pkg]) > keep+2:
                for file in packages[pkg][ : -(keep+2) ]:
                    os.remove(file)
                    print(file, '[kernel > '+str(keep+2)+']')
        else:
            if len(packages[pkg]) > keep:
                for file in packages[pkg][ : -keep ]:
                    os.remove(file)
                    print(file, '[> '+str(keep)+']')

except OSError as e:
    if e.filename:
        print(e.strerror, e.filename, sep=': ', file=sys.stderr)
    else:
        print(e.strerror, file=sys.stderr)

