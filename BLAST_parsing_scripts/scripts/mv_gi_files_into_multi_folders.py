#!/usr/bin/python
#mv_gi_files_into_multi_folders.py
import sys, os, re
from os import listdir
from os.path import isfile, join

if len(sys.argv) != 2:
	print "Usage: python mv_gi_files_into_multi_folders.py <folder containing multiple gi files> \n"
	exit()

mydir = sys.argv[1]
#number_of_files = sys.argv[2]
onlyfiles = [f for f in listdir(mydir) if isfile(join(mydir, f))]

for infile in onlyfiles:
	if re.match(r".+_gi_\d+\.txt",infile):
		obj = re.search(r".+_gi_(\d+)",infile)
		file_order = obj.group(1)
		blast_folder = "blast_" + str(file_order)
		cmd1 = "mkdir " + blast_folder + "\n"
		os.system(cmd1)
		cmd2 = "cp " + infile + " " + blast_folder + "\n"
		os.system(cmd2)



