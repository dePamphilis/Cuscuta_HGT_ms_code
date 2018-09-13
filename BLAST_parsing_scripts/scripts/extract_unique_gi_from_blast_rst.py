#!/usr/bin/python
import sys, os, re, csv
#extract_unique_gi_from_blast_rst.py

if len(sys.argv)!=2:
	print "Usage:  python extract_unique_gi_from_blast_rst.py <blast result> "
	exit()

blast_file = sys.argv[1]
gi_list = list()

with open(blast_file, "r") as f:
	for row in f:
		row = row.rstrip("\n")
		row_list = row.split()
		#print row_list
		hit = row_list[1]
		if re.match(r"^gi\|\d+", hit):
			obj = re.search(r"^gi\|(\d+)\|",hit)
			gi_num = obj.group(1)
			gi_list.append(gi_num)


uniq_list= list(set(gi_list)) 
for gi in uniq_list:
	print str(gi)