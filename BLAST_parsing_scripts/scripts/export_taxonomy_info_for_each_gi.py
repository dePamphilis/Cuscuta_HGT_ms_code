#!/usr/bin/python
import sys, os, re, csv

#export_taxonomy_info_for_each_gi.py
if len(sys.argv)!=3:
    print "Usage:   python export_taxonomy_info_for_each_gi.py <tax_id_and_taxony_info_file> <each gi number and its tax id file>"
    exit()

tax_info_file = sys.argv[1]
gi_taxid_file = sys.argv[2]

tax_info_dict = dict()
header =""

with open(tax_info_file, "r") as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        row_str = "\t".join(row)
        if re.search(r"^\s+",row_str):
            next
        else:
            if re.search(r"^Tax",row_str):
                row[0] = row[0].replace("TaxId","gi_number")
                header = "\t".join(row)
                print header
            else:
                try:
                    id = row[0]
                    info_list = row
                    del info_list[0]
                    info = "\t".join(info_list)
                    tax_info_dict[id] = info
                    #print id + "\t" + info
                except:
                    next
 

with open(gi_taxid_file,"r") as f:
    
    for row in f:
        row = row.rstrip("\n")
        row_list = row.split()
        #print row_list
        try:
            gi = row_list[0]
            tax = tax_info_dict[row_list[1]]
            print gi + "\t" + tax
        except:
            next



