#!/usr/bin/perl

use strict;
use warnings;
use File::Basename qw/basename/;
use File::Find qw/find/;
use File::Path qw/mkpath/;
use File::Copy qw/copy/;
use Getopt::Long;
Getopt::Long::Configure("permute");

my ($verbose, $notorrent, $zeropad, $moveother, $output, $passkey);

##############################################################
# whatmp3 - Convert FLAC to mp3, create what.cd torrent.
# Created by shardz (logik.li)
# Based on: Flac to Mp3 Perl Converter by Somnorific
# Which was based on: Scripts by Falkano and Nick Sklaventitis
##############################################################

### VERSION 2.0

# Do you always want to move additional files (.jpg, .log, etc)?
$moveother = 1;

# Output folder unless specified: ("/home/samuel/Desktop/")
$output = $ENV{HOME} . "/arch/";

# Do you want to zeropad tracknumber values? (1 => 01, 2 => 02 ...)
$zeropad = 1;

# Specify torrent passkey
$passkey = "zs3wkpdvmsouqvlrokz4otf8ndh0xxmg";

# List of default encoding options, add to this list if you want more
my %lame_options = (
	"320" => "-b 320 --ignore-tag-errors",
	"V0"  => "-V 0 --vbr-new --ignore-tag-errors",
	"V2"  => "-V 2 --vbr-new --ignore-tag-errors",
);

###
# End of configuration
###

my (@lame_options, @flac_dirs);

ARG: foreach my $arg (@ARGV) {
	foreach my $opt (keys %lame_options) {
		if ($arg =~ m/\Q$opt/i) {
			push(@lame_options, $opt);
			next ARG;
		}
	}
}

sub process {
	my $arg = shift @_;
	chop($arg) if $arg =~ m'/$';
	push(@flac_dirs, $arg);
}

GetOptions('verbose' => \$verbose, 'notorrent' => \$notorrent, 'zeropad', => \$zeropad, 'moveother' => \$moveother, 'output=s' => \$output, 'passkey=s' => \$passkey, '<>' => \&process);

$output =~ s'/?$'/' if $output;	# Add a missing /

unless (@flac_dirs) {
	print "Need FLAC file parameter\n";
	print "You can specify which lame encoding (V0, 320, ...) you want with --opt\n";
	exit 0;
}

# Store the lame options we actually want.

die "Need FLAC file parameter\n" unless @flac_dirs;

foreach my $flac_dir (@flac_dirs) {
	my (@files, @dirs);
	find( sub { push(@files, $File::Find::name) if ($File::Find::name =~ m/\.flac$/) }, $flac_dir);

	print "Using $flac_dir\n" if $verbose;

	foreach my $lame_option (@lame_options) {
		my $mp3_dir = $output . basename($flac_dir) . " ($lame_option)";
		$mp3_dir =~ s/FLAC//g;
		mkpath($mp3_dir);

		print "\nEncoding with $lame_option started...\n" if $verbose;

		foreach my $file (@files) {
			my (%tags, $mp3_filename);
			my $mp3_dir = $mp3_dir;
			if ($file =~ m!\Q$flac_dir\E/(.+)/.!) {
				$mp3_dir .= '/' . $1;
				mkpath($mp3_dir);
			}

			foreach my $tag (qw/TITLE ALBUM ARTIST TRACKNUMBER GENRE COMMENT DATE/) {
				($tags{$tag} = `metaflac --show-tag=$tag "$file" | awk -F = '{ printf(\$2) }'`) =~ s![:?/]!_!g;
			}

			$tags{'TRACKNUMBER'} =~ s/^(?!0|\d{2,})/0/ if $zeropad;	# 0-pad tracknumbers, if desired.

			if ($tags{'TRACKNUMBER'} and $tags{'TITLE'}) {
				$mp3_filename = $mp3_dir . '/' . $tags{'TRACKNUMBER'} . " - " . $tags{'TITLE'} . ".mp3";
			} else {
				$mp3_filename = $mp3_dir . '/' . basename($file) . ".mp3";
			}

			# Build the conversion script and do the actual conversion
			my $flac_command = "flac -dc \"$file\" | lame $lame_options{$lame_option} " .
				'--tt "' . $tags{'TITLE'} . '" ' .
				'--tl "' . $tags{'ALBUM'} . '" ' .
				'--ta "' . $tags{'ARTIST'} . '" ' .
				'--tn "' . $tags{'TRACKNUMBER'} . '" ' .
				'--tg "' . $tags{'GENRE'} . '" ' .
				'--ty "' . $tags{'DATE'} . '" ' .
				'--add-id3v2 - "' . $mp3_filename . '" 2>&1';
				print "$flac_command\n" if $verbose;
				system($flac_command);
		}

		print "\nEncoding with $lame_option finished...\n";

		if ($moveother) {
			print "Moving other files... " if $verbose;

			find( { wanted => sub {
				if ($File::Find::name !~ m/\.flac$/) {
					if ($File::Find::name =~ m!\Q$flac_dir\E/(.+)/.!) {
						mkpath($mp3_dir . '/' . $1);
						copy($File::Find::name, $mp3_dir . '/' . $1);
					} else {
						copy($File::Find::name, $mp3_dir);
					}
				}
			}, no_chdir => 1 }, $flac_dir);
		}

		if ($output and $passkey and not $notorrent) {
			print "\nCreating torrent... " if $verbose;
			my $torrent_create = 'mktorrent -p -a http://tracker.what.cd:34000/' . $passkey . '/announce -o "' . $output . basename($mp3_dir) . '.torrent" "' . $mp3_dir . '"';
			print "'$torrent_create'\n" if $verbose;
			system($torrent_create);
		}
	}
	print "\nAll done with $flac_dir...\n" if $verbose;
}
