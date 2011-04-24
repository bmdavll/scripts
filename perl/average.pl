#!/usr/bin/perl
# computes the average of each tab-delimited column
use strict;
use warnings;

my $lines = 0;
my @line;
my @sum;
my @tally;

while (<>) {
	$lines++;
	chomp;
	if (not /^(\t|[+-]?(?:\d+\.?|\d*\.\d+))+$/) {
		warn "Misformatted line $lines: $_\n" if /\S/;
		next;
	}
	@line = split("\t");
	foreach my $col (keys @line) {
		if ($line[$col] cmp '') {
			$sum[$col] += $line[$col];
			$tally[$col]++;
		}
	}
}

foreach my $col (keys @tally) {
	if (defined $tally[$col]) {
		print $sum[$col] / $tally[$col];
		print "\t" if $col != $#tally;
	} else {
		print "\t";
	}
}
print "\n";
