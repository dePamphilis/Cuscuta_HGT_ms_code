#!/usr/bin/python
import sys, os, re
#get_nonself_species_nonplant_best_hit.py  #the file has to be sorted already

if len(sys.argv) != 3:
	print "Usage: python get_nonself_species_nonplant_best_hit.py <input_sorted_blast_file> self_species \n\n"
	exit()
sorted_blast = sys.argv[1]
self_species = sys.argv[2]

initial_query = ""
query_top_hit_dict = dict()
with open(sorted_blast,"r") as f:
	for row in f:
		row = row.rstrip("\n")
		row_list = re.split("\t",row)
		#F[11] is bs, F[12] is species, F[13] is Viridiplantae
		field1 = row_list[0]
		field_species = row_list[12]

		if field1 == initial_query:
			initial_query = initial_query
			if field_species == self_species:
				count += 0
			else:
				count += 1
				if count==1:
					#print row + "\t" + str(count)
					query_top_hit_dict[initial_query] = row
				else:
					next
		else:
			initial_query = field1
			count = 0
			if field_species == self_species:
				pass
			else:
				count +=1
				if count==1:
					query_top_hit_dict[initial_query] = row
				else:
					pass

error_file = "error_blast.txt"
outfile_handle = open(error_file, "w")
for key in query_top_hit_dict.keys():
	value = query_top_hit_dict[key]
	value_list = re.split("\t",value)
	#test
	#print value

	#later comment on "print value"
	try:
		if value_list[13] == "Viridiplantae":
			next
		else:
			print value
	except:
		outfile_handle.write(value)
		print


