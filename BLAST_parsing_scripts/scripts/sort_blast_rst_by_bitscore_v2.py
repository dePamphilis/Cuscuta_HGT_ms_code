#!/usr/bin/python
#sort_blast_rst_by_bitscore.py 

from operator import itemgetter
import sys, os, re

if len(sys.argv)!=2:
    print "Usage:   python sort_blast_rst_by_bitscore.py <input file> "
    exit()

infile = sys.argv[1]


query_hit_dict = dict()
query_bs_dict = dict()
query_list = list()

with open(infile,"r") as f:
    for row in f:
        row = row.rstrip("\n")
        row_list = row.split("\t")
        query = row_list[0]
        query_list.append(query)
        #print query

for query in query_list:
    query_hit_dict[query] = dict()
    query_bs_dict[query] = dict()
    #print query


sorted_list = list()
with open(infile,"r") as f:
    for row in f:
        row = row.rstrip("\n")
        row_list = row.split("\t")
        try:
            hit = row_list[1]
            bs = row_list[11]
            bs = bs.strip("\s+")
            bs = float(bs)
            #print row_list
            hit = row_list[1]
            query = row_list[0]
            row_list[11]= float(row_list[11])
            sorted_list.append(row_list)
        except:
            pass
#0,11,1
final_list = sorted(sorted_list,key=itemgetter(0,11,1),reverse=True)

for line in final_list:
    line[11] = str(line[11])
    line_tab =  "\t".join(line)
    print line_tab




