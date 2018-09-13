#!/usr/bin/python
#create_multiple_pbs_tax_classifier_scripts.py

from __future__ import division

"""
the purpose of this script is to create multiple pbs scripts at the same time
"""
import sys, re, os, math, string


if len(sys.argv) !=4:
    print "python create_multiple_pbs_tax_classifier_scripts.py run_directory_without_forwardSlash  prefix   #_of_directories"
    sys.exit()

folder = sys.argv[1]
prefix = sys.argv[2]
total = sys.argv[3]



fasta_dir = ""
filename = ""
line_cd = ""
line_perl = ""

folder_number_upper_bound = int(total) + 1 
for i in range(1,folder_number_upper_bound):
	file_fix = "#PBS -l nodes=1:ppn=6" + "\n"
	file_fix += "#PBS -l walltime=96:00:00" + "\n"
	file_fix += "#PBS -l pmem=8gb" + "\n"
	filename = "run_tax_classifier_" + str(i) + ".phb"
	fasta_dir = folder + "/" + prefix + str(i)
	#print filename
	#print act_dir
	line_cd = "cd" + " " + folder + "\n"
	line_perl = "perl /gpfs/home/zzy5028/biostar/users/zzy5028/Taxonomy/get_taxonomic_info_given_gi_num_biostar_PhAe.pl " + fasta_dir + " 6" + " /gpfs/home/zzy5028/biostar/users/zzy5028/Taxonomy/gi_and_taxonomic_info_rm_empty.txt" + "\n"
	#print line_cd
	#print line_perl
	file_fix += line_cd 
	file_fix += "module load perl/5.10.1" + "\n"
	file_fix += "echo \" \"" + "\n"
	file_fix += "echo " 
	file_fix += "\"Job started on `hostname` at `date`\"" + "\n"
	file_fix += line_perl
	file_fix += "echo \" \"" + "\n"
	file_fix += "echo \"Job Ended at `date`\""+ "\n"
	file_fix += "echo \" \"" + "\n"

	outfile_handle = open(filename,"w")
	outfile_handle.write(file_fix)



for i in range(1,folder_number_upper_bound):
	filename = "run_tax_classifier_" + str(i) + ".phb"
	print "qsub " + filename

