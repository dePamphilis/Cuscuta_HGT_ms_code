#!/usr/bin/perl -w
use strict;
#get_unique_lines.pl
my $infile = $ARGV[0] || die "need input file\n\n";

my %line;
open IN,"<$infile";
while(<IN>) {
	chomp;
	$line{$_} = $_;
}
close IN;

foreach my $key (keys %line) {
	print "$key\n";
}
