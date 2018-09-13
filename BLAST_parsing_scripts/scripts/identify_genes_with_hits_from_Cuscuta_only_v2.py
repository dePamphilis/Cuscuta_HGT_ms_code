#!/usr/bin/python
import sys, os, re
#identify_genes_with_hits_from_Cuscuta_only.py
if len(sys.argv) != 2:
	print "Usage: python identify_genes_with_hits_from_Cuscuta_only.py <input_blast_file> \n\n"
	exit()

blast_file = sys.argv[1]
hit_species_dict = dict()
query_list = list()
with open(blast_file, "r") as f:
	for row in f:
		row = row.rstrip("\n")
		row_list = re.split("\t",row)
		query = row_list[0]
		query_list.append(query)

for query in query_list:
	hit_species_dict[query] = list()

with open(blast_file, "r") as f:
	for row in f:
		row = row.rstrip("\n")
		row_list = re.split("\t",row)
		query = row_list[0]
		temp = row_list[15]
		array = re.split("\s",temp)
		genus = array[0]
		
		hit_species_dict[query].append(genus)
for query in hit_species_dict.keys():
	hit_species_list = hit_species_dict[query]
	hit_species_list_uniq = list(set(hit_species_list))
	if len(hit_species_list_uniq) ==1:
		if hit_species_list_uniq[0] == "Cuscuta":
			print query