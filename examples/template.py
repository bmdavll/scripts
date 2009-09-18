#!/usr/bin/env python3

#########################################################################
#
#   Copyright 2009 David Liang
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   Revisions:
#   2009-04-22  File created
#
#########################################################################

import sys, os, signal

__version__ = "0.1"
__usage__ = "Usage: %prog [options]"
__doc__ = """
"""

__debugging__ = True

def Debug(*args, sep=' ', file=sys.stderr):
    if __debugging__:
        ProgPrint(*args, name="db", sep=sep, file=file)

def Debug(*args, iterate=False, sep=' ', file=sys.stderr):
    if not __debugging__: return
    if iterate:
        for arg in args:
            for item in arg:
                ProgPrint(item, name="db", file=file)
    else:
        ProgPrint(*args, name="db", sep=sep, file=file)

def ProgPrint(*args, name=None, sep=' ', end='\n', file=sys.stdout):
    if name is None:
        name = __prog__
    if len(args) == 0:
        print(file=file, end=end)
    else:
        print(name+': '+sep.join(map(str, args)), end=end, file=file)

def TestPrint(condition, *args, sep=' ', end='\n', file=sys.stdout):
    if condition:
        ProgPrint(*args, sep=sep, end=end, file=file)

def PrintError(*args, sep=': ', end='\n', file=sys.stderr):
    pargs = []
    for arg in args:
        if arg is not None and arg != '':
            pargs.append(arg)
    if pargs:
        ProgPrint(*pargs, sep=sep, end=end, file=file)


class Exit(Exception):

    def __init__(self, status, *args):
        self.status = status
        self.args = args

class Fatal(Exit):

    def __init__(self, *args):
        status = 66

        if len(args) > 0 and isinstance(args[0], int):
            status = args[0]
            args = args[1:]

        if len(args) == 0:
            args = ("fatal error",)

        super().__init__(status, *args)


def handler(signum, frame):
    msg = None

    if signum:
        for signame in ("SIGINT", "SIGQUIT", "SIGABRT"):
            if signum == getattr(signal, signame, None):
                msg="aborted"
        for signame in ("SIGHUP", "SIGTERM"):
            if signum == getattr(signal, signame, None):
                msg="terminated"

    if msg: raise Exit(signum, msg)



def updateStatus(code):
    global _status, _num_errors
    if code == 0:
        _status = 0
        _num_errors = 0
    else:
        _status = max(_status, code)
        _num_errors += 1

def instantiateGlobals():
    global _rundir
    _rundir = os.getcwd()

def parseOptions(argv):

    from optparse import OptionParser, OptParseError
    class OptParser(OptionParser):
        def error(self, msg):
            raise OptParseError(msg)
        def exit(self, status=0, msg=None):
            raise Exit(status, msg)
    try:
        parser = OptParser(prog=__prog__, version="%prog "+__version__,
                           usage=__usage__, add_help_option=False)
        parser.add_option("-h", "--help", default=False, action="store_true",
                          help='show this help message and exit')
        parser.add_option("-?", "--usage", default=False, action="store_true",
                          help='show a brief usage string and exit')

        opts, args = parser.parse_args(argv[1:])

        if opts.help:
            parser.print_version()
            print(__doc__ % globals())
            print()
            parser.print_help()
            raise Exit(0, None)
        elif opts.usage:
            parser.print_usage()
            raise Exit(0, None)

        if len(args) == 0:
            raise OptParseError(None)

        return args

    except OptParseError as e:
        parser.print_usage(file=sys.stderr)
        raise Exit(2, e.msg)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    signals = ("SIGINT", "SIGQUIT", "SIGABRT", "SIGHUP", "SIGTERM")
    saved_handlers = {}
    for signame in signals:
        signum = getattr(signal, signame, None)
        if signum:
            saved_handlers[signum] = signal.signal(signum, handler)
    try:
        global __prog__
        __prog__ = os.path.basename(argv[0])

        updateStatus(0)
        instantiateGlobals()

        args = parseOptions(argv)


        return _status

    except Exit as e:
        PrintError(*e.args)
        return e.status

    finally:
        pass

        for signum in saved_handlers:
            signal.signal(signum, saved_handlers[signum])


if __name__ == '__main__':
    sys.exit(main())

