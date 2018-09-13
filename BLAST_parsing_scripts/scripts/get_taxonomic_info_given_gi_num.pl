#!/usr/bin/perl -w
# ===============================================
# 
# NOTE: Please check the number of processors (n) 
# on your machines - don't exceed n-1 processors

# ===============================================

use strict;
use threads;
use threads::shared;

# ============= Check for input parameters =========
if (!$ARGV[1]) {
    print "USAGE:get_taxonomic_info_given_gi_num.pl <id_directory> <processors>  <gi_and_taxonomic_info_rm_empty.txt> \n";
    exit(1);
}

# ============ Initialize varibles ============
my $gi_dir="$ARGV[0]"; # /path_to/fasta_files_dir
my $th="$ARGV[1]";  # e.g 6
my $big_file = "$ARGV[2]";
my @files;

print "START getting taxonomy information from the big file $gi_dir...\n\n";
my $count = 0;
opendir (DIR, "$gi_dir") or die "Couldn't open $gi_dir directory, $!";

while (my $file = readdir(DIR)) {
    if ($file !~ /Cuscuta_blast_rst_gi_numbers.+_\d+\.txt$/) {next;}  # change pattern to match your fasta files
    push (@files, $file);
}
closedir(DIR);

my $dirname ="$gi_dir/Tax_info_results";
mkdir $dirname, 0755;
my @sub_files;

for (my $i = 0; $i <= $#files; $i++){
    if (($#sub_files+1) <= $th){ push(@sub_files, $files[$i]);}
    if ((($#sub_files+1) == $th) or ($i == $#files)){
        my @threads;
        for ( my $count = 1; $count <= $#sub_files+1; $count++) {
           # my $t = threads->new(\&run_blast_commands, "blastall -p blastp -d /home/shared/Projects/Zhenzhen/blast/database/HGT.orthos.fasta.faa -i $gi_dir/$sub_files[$count-1] -o $dirname/$sub_files[$count-1].blastp -m 8 -e 1e-10 -b 5 -v 5");
           my $t = threads->new(\&run_blast_commands,"python ~/Dropbox/BACKUP/Bioinformatics_journal/python/export_whole_line_info_of_given_id_v2_faster.py $big_file $gi_dir/$sub_files[$count-1] > $dirname/$sub_files[$count-1].and.taxonomicinfo.txt");
            push(@threads,$t);
        }
        foreach (@threads) {
            $_->join;
        }
        @sub_files = ();        
    }
} 


system "cat $dirname/* > taxonomy_info.txt";   
print "DONE RUNNING MULTIPLE GETTING TAXONOMY INFO IN $gi_dir...\n\n";
print "Combined taxonomy information in taxonomy_info.txt file\n\n";
exit;

sub run_blast_commands{
    my ($system_call) = @_;
    system $system_call;
}


