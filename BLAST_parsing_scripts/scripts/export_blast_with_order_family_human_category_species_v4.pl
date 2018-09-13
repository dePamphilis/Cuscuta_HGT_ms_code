#!/usr/bin/perl -w
use strict;
#export_blast_with_order_family_human_category_species_v4.pl

#make sure that you have these scripts in the current running directory
#plant_subclass_and_human_curated_category,F15_nothing_F14_and_human_curated_category_and_other_info, plant_non-typical_order_and_human_curated_category
my $sorted_blast = $ARGV[0]; 

my %order_cat; 
my %class_cat;

my $order = ""; 
my $family = ""; 
my $species = "";
my $class = ""; 
my $non_typ_order =""; 
my $human_category = ""; 

my %empty15_order;
my %empty15_family;
my %empty15_curated_cat;

my %check_para;
$check_para{"Alectra"} = "_para_Orobanchaceae";
$check_para{"Balanophora"} = "_para_Santalales";
$check_para{"Daenikera"} = "_para_Santalales";
$check_para{"Dendropemon"} = "_para_Santalales";
$check_para{"Epifagus"} = "_para_Orobanchaceae";
$check_para{"Exocarpos"} = "_para_Santalales";
$check_para{"Orobanche"} = "_para_Orobanchaceae";
$check_para{"Phelipanche"} = "_para_Orobanchaceae";
$check_para{"Phoradendron"} = "_para_Santalales";
$check_para{"Pilostyles"} = "_para_Apodanthaceae";
$check_para{"Santalum"} = "_para_Santalales";
$check_para{"Striga"} = "_para_Orobanchaceae";
$check_para{"Triphysaria"} = "_para_Orobanchaceae";
$check_para{"Ximenia"} = "_para_Orobanchaceae";


print "query\thit\tperc_identity\talignment_length\tmismatches\tgap_opens\tquer_start\tquery_end\thit_start\thit_end\tevalue\tbitscore\torder\tfamily\tcurated_category\tspecies\n";
open OR, "<plant_non-typical_order_and_human_curated_category";
while (<OR>) {
	chomp;
	my @F=split(/\t/,$_); 
	$F[1] =~ s/\s+$//;
	$order_cat{$F[0]} = $F[1];
}
close OR;

open CLASS, "<plant_subclass_and_human_curated_category";
while(<CLASS>) {
	chomp;
	my @F=split(/\t/,$_); 
	$F[1] =~ s/\s+$//;
	$class_cat{$F[0]} = $F[1];
}
close CLASS;

open EM, "<F15_nothing_F14_and_human_curated_category_and_other_info";
while (<EM>) {
	chomp;
	my @F=split(/\t/,$_); 
	$empty15_order{$F[0]} = $F[1];
	$empty15_family{$F[0]} = $F[2];
	$empty15_curated_cat{$F[0]} = $F[5];

}
close EM;

# my %empty15_order;
# my %empty15_family;
# my %empty15_curated_cat;

open IN, "<$sorted_blast";
while (<IN>) {
	chomp;

	my $order = ""; 
	my $family = ""; 
	my $species = "";
	my $class = ""; 
	my $non_typ_order =""; 
	my $human_category = ""; 
	my $out=""; 
	my @F=split(/\t/,$_); 
	$species = $F[12];
	if (!$F[15]) {
		if (!$F[14]) {
			$species = $F[12];
			my @S = split(/\s+/,$species);
			$family = $S[0]; #here family is actually class, which can consist of several families, but it's okay within green algae
			if ($family eq 'Trebouxiophyceae') {
				$order  = "NA";
				$human_category = "green algae";
			}
			if ($family eq 'Prasinophyceae') {
				$order  = "NA";
				$human_category = "green algae";
			}
			if ($family eq 'marchantiophyte') {
				$order  = "NA";
				$human_category = "liverworts";
			}
			
		}
		else {
			$family = $empty15_family{$F[14]};
			$order = $empty15_order{$F[14]};
			$human_category = $empty15_curated_cat{$F[14]};

		}
	}
	elsif ($F[15] =~ /ales$/) {
		$order = $F[15];
		$class = $F[14];
		$human_category = $class_cat{$class};
		for my $i (16..$#F) {
			if ($F[$i] =~ /ceae$/) {
				$family = $F[$i];
			}
		}
	}
	else {
		for my $i (12..$#F) {
			if ($F[$i] =~ /ales$/) {
				$order = $F[$i];
				$non_typ_order = $F[$i];
				$human_category = $order_cat{$non_typ_order};
				for my $j ($i..$#F) {
					if ($F[$j] =~ /ceae$/) {
						$family = $F[$j];
					}
				}
			}

			elsif ($F[$i] eq "Botryococcaceae") {
				$family = $F[$i];
				$order  = "NA";
				$human_category = "green algae";
			}
			elsif ($F[$i] eq "Coccomyxaceae") {
				$family = $F[$i];
				$order  = "Chlorococcales";
				$human_category = "green algae";
			}
			elsif ($F[$i] eq "Microsporaceae") {
				$family = $F[$i];
				$order  = "NA";
				$human_category = "green algae";
			}
			elsif ($F[$i] eq "Pycnococcaceae") {
				$family = $F[$i];
				$order  = "NA";
				$human_category = "green algae";
			}
#Icacinaceae	Icacinales	asterids
#Vahliaceae	Vahliales	asterids
#Dasypogonaceae	Arecales	monocots
#Oncothecaceae	Icacinales	asterids
			elsif ($F[$i] eq "Icacinaceae") {
				$family = $F[$i];
				$order  = "Icacinales";
				$human_category = "asterids";
			}
			elsif ($F[$i] eq "Vahliaceae") {
				$family = $F[$i];
				$order  = "Vahliales";
				$human_category = "asterids";
			}
			elsif ($F[$i] eq "Dasypogonaceae") {
				$family = $F[$i];
				$order  = "Arecales";
				$human_category = "monocots";
			}
			elsif ($F[$i] eq "Oncothecaceae") {
				$family = $F[$i];
				$order  = "Icacinales";
				$human_category = "asterids";
			}
		}
	}

	for my $i (0..11) {
		$out .= "$F[$i]\t";
	}
	my @M = split(/\s+/,$species);
	if (defined $M[0]) {

		my $genus = $M[0];
		#test
		#print "$genus\n";
		if (defined $check_para{$genus}) {
			$family .= $check_para{$genus};
		}
	}
	
	$out.= "$order\t$family\t$human_category\t$species\n";
	print "$out";

}
close IN;
