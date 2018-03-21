#!/usr/bin/python
#calculate_3weights_per_gene_Cuscuta.py
#This script will export an output file containing the proportion of each gene from self, close, and various distant taxonomic groups
#This script needs to accept two input files, one is a BLAST input file, the other is the taxonomic group information of each order
#The order information is also present in the BLAST input file. In essence, the BLAST input file has the tabular BLAST output information
#and concatenated taxonomic information of the hit, for instance, the species, the order, the genus, and etc
#an example of the <BLAST input file> is provided as "input_file1_example_blast_input", an example of the <order and group file> is provided as "input_file2_order_and_human_curated_category_input.txt".

import sys, os, re

if len(sys.argv) <3:
	print "Usage::: python calculate_3weights_per_gene_Cuscuta.py <blast_file> <order_and_group_file>"
	exit()


infile = sys.argv[1]
order_and_group_file = sys.argv[2]

group_dict = dict()

with open(order_and_group_file, "r") as f:
	for row in f:
		row = row.rstrip("\n")
		row_list = re.split("\t",row)
		order = row_list[0]
		group = row_list[2]
		group_dict[order] = group

query_list = list()

#this stores the counts
self_dict = dict()
close_dict= dict()
distal_rosid_dict = dict()
distal_monocot_dict = dict()
distal_basal_dict = dict()
distal_gymnosperm_dict = dict()
distal_non_seed_dict = dict()

#this stores the proportion
self_propor_dict = dict()
close_propor_dict= dict()
distal_rosid_propor_dict = dict()
distal_monocot_propor_dict = dict()
distal_basal_propor_dict = dict()
distal_gymnosperm_propor_dict = dict()
distal_non_seed_propor_dict = dict()

with open(infile, "r") as f:
	for row in f:
		row = row.rstrip("\n")
		row_list = re.split("\t",row)
		query = row_list[0]
		query_list.append(query)

query_list_uniq = set(query_list)

for query in query_list_uniq:
	#test
	#print query 
	self_dict[query] = float(0)
	close_dict[query] = float(0)
	distal_rosid_dict[query] = float(0)
	distal_monocot_dict[query] = float(0)
	distal_basal_dict[query] = float(0)
	distal_gymnosperm_dict[query] = float(0)
	distal_non_seed_dict[query] = float(0)

current_line_num = 0
query_top50hitNum_dict = dict()
current_query = ""

#temp_list = list()
with open(infile, "r") as f:
	for row in f:
		#line_num += 1 
		if row.startswith("query"):
			#print "yes"
			pass
		else:
			row = row.rstrip("\n")
			row_list = re.split("\t",row)
			query = row_list[0]
			#print query
			if not query == current_query:
				current_query = query
				current_line_num = 1
			else:
				current_line_num += 1


			#temp_list.append(query) 
			#print current_query

			if current_line_num <=50:
				#print "yes"
				try:
					if row_list[11]:
						#print "yes"


						family = row_list[16]
						genus = row_list[-1]
						order = row_list[15]
						species = row_list[12]

						#print family + "\t" + order + "\t" + genus
						group = group_dict[order]
						
						#print  query + "\t" + str(current_line_num)

						if group == "close":
							if family.startswith("Orobanchaceae"):
								#print "yes"
								pass
							else:
								close_dict[query] += 1
						elif group == "close_or_self":

							#print "yes"
							if genus == "Cuscuta":
								self_dict[query] += 1
							else:
								close_dict[query] += 1
						elif group == "distant_rosid":
							distal_rosid_dict[query] += 1
						elif group == "distant_monocot":
							distal_monocot_dict[query] += 1
						elif group == "distant_basal":
							distal_basal_dict[query] += 1
						elif group == "distant_gymnosperm":
							distal_gymnosperm_dict[query] += 1
						elif group == "distant_non-seeed_plant":
							distal_non_seed_dict[query] += 1


						query_top50hitNum_dict[query] = current_line_num

				except:
					pass
					
			else:
				pass
# for query in query_top50hitNum_dict.keys():
# 	print str(query_top50hitNum_dict[query]) + "\t" + query

# self_propor_dict = dict()
# close_propor_dict= dict()
# distal_rosid_propor_dict = dict()
# distal_monocot_propor_dict = dict()
# distal_basal_propor_dict = dict()
# distal_gymnosperm_propor_dict = dict()
# distal_non_seed_propor_dict = dict()
# query_top50hitNum_dict = dict()


header = "query\tself_propor_top50\tclose_propor_top50\tdistal_rosid_propor_top50\tdistal_monocot_propor_top50\tdistal_basal_propor_top50\tdistal_gymnosperm_propor_top50\tdistal_non_seed_propor_top50" 
print header

# temp_list_u = set(temp_list)
# for query in temp_list_u:
# 	print query
for query in self_dict.keys():
	if query == "query":
		pass
	else:

	#print query + "\t" + str(self_dict[query])

		self_propor_dict[query] = self_dict[query]/query_top50hitNum_dict[query]
		close_propor_dict[query] = close_dict[query]/query_top50hitNum_dict[query]
		distal_rosid_propor_dict[query] = distal_rosid_dict[query]/query_top50hitNum_dict[query]
		distal_monocot_propor_dict[query] = distal_monocot_dict[query]/query_top50hitNum_dict[query]
		distal_basal_propor_dict[query] = distal_basal_dict[query]/query_top50hitNum_dict[query]
		distal_gymnosperm_propor_dict[query] = distal_gymnosperm_dict[query]/query_top50hitNum_dict[query]
		distal_non_seed_propor_dict[query] = distal_non_seed_dict[query]/query_top50hitNum_dict[query]

		out = ""
		out += query + "\t" + str(self_propor_dict[query]) + "\t" + str(close_propor_dict[query]) + "\t" + str(distal_rosid_propor_dict[query]) + "\t"
		out +=  str(distal_monocot_propor_dict[query]) + "\t" + str(distal_basal_propor_dict[query]) + "\t" + str(distal_gymnosperm_propor_dict[query]) + "\t" + str(distal_non_seed_propor_dict[query])
		print out 


