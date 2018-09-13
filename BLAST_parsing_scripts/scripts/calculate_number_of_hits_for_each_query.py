#!/usr/bin/python
import sys, os, re
#calculate_number_of_hits_for_each_query.py  #the file has to be sorted already

if len(sys.argv) != 2:
	print "Usage: python calculate_number_of_hits_for_each_query.py <input_blast_file> \n\n"
	exit()
blast_file = sys.argv[1]
hit_dict = dict()
query_list = list()
with open(blast_file, "r") as f:
	for row in f:
		row = row.rstrip("\n")
		row_list = re.split("\t",row)
		query = row_list[0]
		hit = row_list[1]
		query_list.append(query)
for query in query_list:
	hit_dict[query] = list()

with open(blast_file, "r") as f:
	for row in f:
		row = row.rstrip("\n")
		row_list = re.split("\t",row)
		query = row_list[0]
		hit = row_list[1]
		hit_dict[query].append(hit)


for query in hit_dict.keys():
	hit_list = hit_dict[query]
	hit_list_uniq = list(set(hit_list))
	hit_size = len(hit_list_uniq)
	print query + "\t" + str(hit_size)
