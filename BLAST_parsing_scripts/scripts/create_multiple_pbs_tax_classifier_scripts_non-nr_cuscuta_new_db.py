#!/usr/bin/python
#create_multiple_pbs_tax_classifier_scripts_non-nr.py

from __future__ import division
from os import listdir
from os.path import isfile, join

"""
the purpose of this script is to create multiple pbs scripts at the same time
"""
import sys, re, os, math, string


if len(sys.argv) !=3:
    print "python create_multiple_pbs_tax_classifier_scripts_non-nr.py run_directory_without_forwardSlash     #_of_files"
    sys.exit()

folder = sys.argv[1]
total = sys.argv[2]

onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

gi_dir = ""
filename = ""
line_cd = ""
line_perl = ""

folder_number_upper_bound = int(total) + 1 
for i in range(1,folder_number_upper_bound):
	file_fix = "#PBS -l nodes=1:ppn=1" + "\n"
	file_fix += "#PBS -l walltime=96:00:00" + "\n"
	file_fix += "#PBS -l pmem=7gb" + "\n"
	filename = "run_tax_non_nr_" + str(i) + ".phb"
	
	#print filename
	#print act_dir
	line_cd = "cd" + " " + folder + "\n"
	for infile in onlyfiles:
		if re.match(r".+_\d+\.txt",infile):
			obj = re.search(r".+_(\d+)\.txt",infile)
			index = obj.group(1)
			if str(index) == str(i):
				infile_path = folder + "/" + infile
				outfile_path = folder + "/tax_" + str(i)
				line_perl = "python /gpfs/home/zzy5028/biostar/users/zzy5028/Tax_non-nr/concatenate_taxonomic_info_for_1kp_and_genomic_hit_with_blast_out_v5_16g4t.py " + infile_path + "  > " + outfile_path + "\n"
				#print line_perl
				file_fix += line_cd 
				file_fix += "module load python" + "\n"
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
	filename = "run_tax_non_nr_" + str(i) + ".phb"
	print "qsub " + filename

