#list A contains listB, this script is to create list A-listB
#the idea is to create a hash for listB
#!/usr/bin/perl -w
use strict;
my $ListA =$ARGV[0] || die "need big list file";
my $ListB =$ARGV[1] || die "need small list file";
my %LB;

open LB,"<$ListB";
while(<LB>) {
    chomp;
    $LB{$_}=$_;
}
close LB;

open LA,"<$ListA";
while(<LA>) {
    chomp;
    if($LB{$_}) {next;}
    print "$_\n";
}
close LA;
