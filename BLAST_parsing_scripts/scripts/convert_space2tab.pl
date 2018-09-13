#!/usr/bin/perl
$infile = $ARGV[0];
open IN, "<$infile";
while(<IN>) {
chomp;
s/\s+/\t/g;
print "$_\n";
}

close IN;

