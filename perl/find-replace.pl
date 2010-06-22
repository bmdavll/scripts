#!/usr/bin/env perl
=pod

Description:
This script does find and replace on a given folder recursively.

Features:
* Multiple Find and Replace string pairs can be given.
* The find/replace strings can be set to regex or literal.
* Files can be filtered according to file name suffix matching or other
  criterion.
* Backup copies of original files will be made at a user specified
  folder that preserves all folder structures of original folder.
* A report will be generated that indicates which files has been
  changed, how many changes, and total number of files changed.
* Files will retain their own/group/permissions settings.

Usage:
1. Edit the parts under the section '#-- arguments --'.
2. Edit the subroutine fileFilterQ to set which file will be checked or
   skipped.

To do:
* In the report, print the strings that are changed, possibly with
  surrounding lines.
* Allow just find without replace.
* Add the GNU syntax for unix command prompt.
* Report if backup directory exists already, or provide toggle to
  overwrite, or some other smarties.

Date created: 2000/02
Author: Xah Lee, XahLee.org
=cut

#-- modules --

use strict;
use File::Find;
use File::Path;
use File::Copy;
use Data::Dumper;

#-- arguments --

# the folder to search in
my $folderPath = q[/home/david/tmp/sandbox];

# backup folder path
my $backupFolderPath = q[/tmp];

my %findReplaceH = (
    q[foo] => q[bar],
    q[this] => q[that],
);

# if 1, intepret the pairs in %findReplaceH as regex
my $useRegexQ = 0;

# in bytes; larger files will be skipped
my $fileSizeLimit = 500 * 1024;


#-- globals --

$folderPath =~ s[/+$][];        # e.g. '/home/joe/public_html'
$backupFolderPath =~ s[/+$][];  # e.g. '/tmp/joe_back'

$folderPath =~ m[/(\w+)$];
my $previousDir = $`;           # e.g. '/home/joe'
my $lastDir = $1;               # e.g. 'public_html'
my $backupRoot = $backupFolderPath . '/' . $1;
                                # e.g. '/tmp/joe_back/public_html'
my $refLargeFiles = [];
my $totalFileChangedCount = 0;

#-- subroutines --

# fileFilterQ($fullFilePath) returns true if file is chosen
sub fileFilterQ ($) {
    my $fileName = $_[0];

    if ((-s $fileName) > $fileSizeLimit) {
        push (@$refLargeFiles, $fileName);
        return 0;
    }
    if ($fileName =~ m/\.html$/) {
        print "processing: $fileName\n";
        return 1;
    }
    # if (-d $fileName) { return 0 }        # directory
    # if (not (-T $fileName)) { return 0 }  # not text file
    return 0;
}

# go thru each file and accumulate a hash
sub processFile {
    my $currentFile = $File::Find::name;    # full path spec
    my $currentDir = $File::Find::dir;
    my $currentFileName = $_;

    if (not fileFilterQ($currentFile)) {
        return 1;
    }

    # open file; read the whole file
    open(FILE, "<$currentFile") or die("error opening file: $!");
    my $wholeFileString;
    {
        local $/ = undef;
        $wholeFileString = <FILE>;
    }
    close(FILE) or die("error closing file: $!");

    # do the replacement
    my $replaceCount = 0;

    foreach my $key1 (keys %findReplaceH) {
        my $pattern = ($useRegexQ ? $key1 : quotemeta($key1));
        $replaceCount = $replaceCount +
                        $wholeFileString =~ s/$pattern/$findReplaceH{$key1}/g;
    }

    if ($replaceCount > 0) {
        $totalFileChangedCount++;
        # do backup
        # make a directory in the backup path; make a backup copy
        my $pathAdd = $currentDir;
        $pathAdd =~ s[$folderPath][];
        mkpath("$backupRoot/$pathAdd", 0, 0777) or die;
        copy($currentFile, "$backupRoot/$pathAdd/$currentFileName") or
            die "error: file copying failed for $currentFile\n$!";

        # write to the original
        # get the file mode
        my ($mode, $uid, $gid) = (stat($currentFile))[2,4,5];

        # write out a new file
        open(OUTFILE, ">$currentFile") or die("error opening file: $!");
        print OUTFILE $wholeFileString;
        close(OUTFILE) or die("error closing file: $!");

        # set the file mode
        chmod($mode, $currentFile);
        chown($uid, $gid, $currentFile);

        print "$currentFile: $replaceCount replacements made\n";
    }
}


#-- main --

find(\&processFile, $folderPath);

print "$totalFileChangedCount files changed\n";

if (scalar @$refLargeFiles > 0) {
    print "\nlarge files skipped:\n";
    print Dumper($refLargeFiles);
}

__END__
