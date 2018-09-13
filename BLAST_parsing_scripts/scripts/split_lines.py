#!/usr/bin/python
#split_lines.py
from __future__ import division
import sys, os, string, re, math

#purpose of this script is to split a file into many small files
#for instance, each small file is 1000 lines

if len(sys.argv)!=3:
	print "Usage python split_lines.py infile	#_of_lines_in_each_file"
	exit()

infile = sys.argv[1]
num_of_lines = sys.argv[2]

file_line_sum = 0 
with open(infile,"r") as f:
	file_line_sum = 0
	for row in f:
		row = row.rstrip("\n")
		if re.search(r"^\S+",row):
			file_line_sum +=1
#print file_line_sum
temp = int(file_line_sum)/int(num_of_lines)
#print temp
num_of_files= int(math.ceil(int(file_line_sum)/int(num_of_lines)))
#print num_of_files

name_dict = dict()
for i in range(1, num_of_files+1):

	name = infile + "_" + str(i) +".txt"
	#print name
	name_dict[i] = name

for index in name_dict.keys():
	name = name_dict[index]
	with open(name,"w") as o:
		with open(infile,"r") as f:
			i = 0
			for row in f:
				row=row.rstrip("\n")
				if re.search(r"^\S+",row):
					i += 1
					file_index = int(math.ceil(int(i)/int(num_of_lines)))
					if file_index == index:
						o.write(row)
						o.write("\n")
			#print str(i) + "\t" + str(file_index)

