#!/usr/bin/env perl
# use strict;
# use warnings;

# Run this script periodically to remove old duplicate commands from your
# bash history file ($HISTFILE).

my @args = grep { $_ !~ /^-/ } @ARGV;
my @opts = grep { $_ =~ /^-/ } @ARGV;

my $histfile = $ENV{HISTFILE} || $args[0];

-f $histfile or die '$HISTFILE not found', "\n",
'Check that "export HISTFILE" is in your .bashrc', "\n";

open HISTFILE, '+<', $histfile or die $histfile, ': ', $!, "\n";

my %seen;
my @unique;

if (grep { $_ eq '--squash' } @opts) {
    @unique = reverse grep { s/\s+$/\n/;
                             s/ {2,}/ /g;
                             not $seen{ $_ }++ } reverse <HISTFILE>;
} else {
    @unique = reverse grep { not $seen{ $_ }++ } reverse <HISTFILE>;
}

truncate HISTFILE, 0;
seek HISTFILE, 0, 0;
print HISTFILE @unique;
