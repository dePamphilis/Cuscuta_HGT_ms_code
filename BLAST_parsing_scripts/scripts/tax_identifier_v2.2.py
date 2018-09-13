#!/usr/bin/python

from urllib2 import HTTPError
#import entrez module
import sys
from Bio import Entrez
import time

# get arguments
args = sys.argv[1]
#print args

# check input arguments
if len(args) < 1:
    print "Expect at least one tax id as an input argument"
    sys.exit()
#f=open(args, mode="r")
taxids=[line.strip() for line in open(args,"r")]
#lines = f.readlines()

failed_list = list()

# set variables
#taxids = [515482, 515474]
#taxids = args

#print taxids

# set email
#Entrez.email = "yangzhenzhen1988@gmail.com"

# traverse ids
#for taxid in taxids:
print "TaxId" + "\t" + "ScientificName" + "\t" + "kingdom" + "\t" + "subclass" + "\t" + "order" + "\t" + "family" + "\t" + "genus"

def get_lineage(ID):
    try:

        handle = Entrez.efetch(db="taxonomy", id=ID, mode="text", rettype="xml")
        records = Entrez.read(handle)
        for taxon in records:
            #taxid = taxon["TaxId"]
    	    final = ID + "\t"
            name = taxon["ScientificName"]
            final = final + name + "\t"
            for t in taxon["LineageEx"]:
    		#one can print this out to get the detailed taxonomic information
    		#print(t)
                try:
            		if t['Rank'] == 'kingdom':
            			#print(t['ScientificName'])
            			final = final + t['ScientificName'] + "\t"
                except:
                    final = final + "\t" + "\t"

                try:

            		if t['Rank'] == 'subclass':
            			#print(t['ScientificName'])
            			final = final + t['ScientificName'] + "\t"
                except:
                    final = final + "\t" + "\t"

                try:

            		if t['Rank'] == 'order':
            			#print(t['ScientificName'])
            			final = final + t['ScientificName'] + "\t"
                except:
                    final = final + "\t" + "\t"

                try:

                    if t['Rank'] == 'family':
                                    #print(t['ScientificName'])
            			final = final + t['ScientificName'] + "\t"
                except:
                    final = final + "\t" + "\t"
                try:
                    if t['Rank'] == 'genus':
                                #print(t['ScientificName'])
        			    final = final + t['ScientificName']
                except:
                    final = final + "\t" + "\t"

            print final
            time.sleep(1)
    except:
        next

Entrez.email = "yangzhenzhen1988@gmail.com"

for taxid in taxids:
    try:
        get_lineage(taxid)
    except:
        failed_list.append(gi)
        if HTTPError:
            print "Error fetching", id
            time.sleep(5) # we have angered the API! Try waiting longer?
            try:
                get_lineage(taxid)
            except:
                with open('error_records.bad','a') as f:
                    f.write(str(id)+'\n')
                continue

failed_list_file = "failed_list" + args
out_h = open(failed_list_file, "w")
for gi in failed_list:
    out = gi + "\n"
    out_h.write(out)