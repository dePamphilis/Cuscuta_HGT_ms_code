#!/usr/bin/perl -w
use strict;
use List::MoreUtils qw(uniq);
#export_tree_file_from_given_ortho_ids.pl
my $infile = "$ARGV[0]" || die "need the input HGT screen output file\n";
my @ortho_list ;
open IN,"<$infile";
while(<IN>) {
    chomp;
    if (/^Orthogroup\s+number/) {
    	$_ =~ /^Orthogroup\s+number.+\s+(\d+)\s+/;
    	#print "$1\n";
    	push @ortho_list, $1;
    }
}
close IN;

my @ortho_list_uniq = uniq @ortho_list;
for my $ortho (@ortho_list_uniq) {
	print "$ortho\n";
}