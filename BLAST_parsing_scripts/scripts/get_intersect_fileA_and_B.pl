#this script is to get the intersect of listA and listB
#!/usr/bin/perl -w
use strict;
my $listA =$ARGV[0] || die "need list A file";
my $listB=$ARGV[1] || die "need listB file";
my %LB;

open IN1,"<$listB";
while(<IN1>) {
    chomp;
    $LB{$_}=$_;
}
close IN1;

open IN2,"<$listA";
while(<IN2>) {
    chomp;
    if($LB{$_}) {
        print "$_\n";
    }  
}
close IN2;
