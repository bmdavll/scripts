#!/usr/bin/python3

import os, re, sys
from glob import glob
from collections import defaultdict
from subprocess import Popen, PIPE

re_suffix = re.compile(r'-[^-]+-[^-]+(-(?:i686|x86_64|any))?\.pkg\.tar\.\w+$')

keep = 3

if sys.argv.count('-h')+sys.argv.count('--help') > 0:
    print(os.path.basename(sys.argv[0]) + ' [keep_num]')
    sys.exit(0)
elif len(sys.argv) == 2 and re.match(r'^[1-9][0-9]*$', sys.argv[1]):
    keep = int(sys.argv[1])

kernel_keep = keep+3

cache_dir = ''

try:
    with open('/etc/pacman.conf') as conf:
        for line in conf:
            mat = re.search('CacheDir\s*=\s*(/.*)', line)
            if mat:
                cache_dir = mat.group(1)
                break
except IOError as e:
    print(e.strerror, file=sys.stderr)
    sys.exit(1)

if not cache_dir:
    cache_dir = '/var/cache/pacman/pkg'

packages = defaultdict(lambda:[])
init = False

def init_print():
    global init
    if not init:
        init = True
        print('Removing old packages from pacman cache ['+cache_dir+']:')

try:
    output = Popen(['pacman', '-Qq'], stdout=PIPE).communicate()[0]
    installed = set(output.decode().split())

    os.chdir(cache_dir)

    files = glob('*')
    files.sort()

    for file in files:
        packages[ re_suffix.sub('', file) ].append(file)

    for pkg in packages:

        if pkg not in installed:
            init_print()
            for file in packages[pkg]:
                os.remove(file)
                print(file, '[not installed]')

        elif pkg.startswith('kernel'):
            if len(packages[pkg]) > kernel_keep:
                init_print()
                for file in packages[pkg][ : -kernel_keep ]:
                    os.remove(file)
                    print(file, '[kernel] [>'+str(kernel_keep)+' available]')
        else:
            if len(packages[pkg]) > keep:
                init_print()
                for file in packages[pkg][ : -keep ]:
                    os.remove(file)
                    print(file, '[>'+str(keep)+' available]')

except OSError as e:
    if e.filename:
        print(e.strerror, e.filename, sep=': ', file=sys.stderr)
    else:
        print(e.strerror, file=sys.stderr)
    sys.exit(1)

