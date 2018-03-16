#!/usr/bin/python
##########################################################################################
#



#difference between v3 and v2_edit is that in v3, the node2 has to be inside the current node (ancestor_1) that the program is traversing
#this is because the first ancestral node (node1) and the second ancestral node (node2) are not restricted by the conditions (mono-left, and mono-right >0)
#it's supposed to be more restrict
##########################################################################################
import sys, os, string, re
#from ete2 import PhyloTree
class SuppressAllOutput (object):
    def __enter__(self):
        sys.stderr.flush()
        self.old_stderr = sys.stderr
        sys.stderr = open('/dev/null', 'a+', 0)
        sys.stdout.flush()
        self.old_stdout = sys.stdout
        sys.stdout = open('/dev/null', 'a+', 0)
 
    def __exit__(self, exc_type, exc_value, traceback):
        sys.stderr.flush()
        sys.stderr = self.old_stderr
        sys.stdout.flush()
        sys.stdout = self.old_stdout
 
print >>sys.stdout, "printing to stdout before suppression"
print >>sys.stderr, "printing to stderr before suppression"
         
with SuppressAllOutput():
    try:
        from ete2 import PhyloTree
        from ete2 import Tree
        print >>sys.stdout, "printing to stdout during suppression"
        print >>sys.stderr, "printing to stderr during suppression"
    except:
        pass
    try:
        from ete3 import PhyloTree
        from ete3 import Tree
        print >>sys.stdout, "printing to stdout during suppression"
        print >>sys.stderr, "printing to stderr during suppression"
    except:
        pass
         
print >>sys.stdout, "printing to stdout after suppression"
print >>sys.stderr, "printing to stderr after suppression"

# check for user input - tree directory
if (len(sys.argv) != 2 ):
	print "get_HGT_from_rosids2Amborella.py <newick_trees_dir>"
	exit()
	
# create output directory
events_dir = '%s''/events' % (str(sys.argv[1]))
if not os.path.exists(events_dir):
	os.makedirs(events_dir)
	
# get tree files from directory
tree_files = os.listdir(str(sys.argv[1]))
for tree in tree_files:
    if re.match(r"^\d+\.fna\.aln.+\.tree",tree):
    	# get orthogroup id
    	ortho = re.sub(r'\D', "", tree)  
        # load newick tree
        #print(tree)
        t = PhyloTree(tree)
        #print(t)
        evts = file('%s''/''%s''.temp' %(events_dir,tree), "w")
##########################################################################################
# 			evolutionary events involving all taxa
##########################################################################################
        # Alternatively, you can scan the whole tree topology
        events = t.get_descendant_evol_events()
        # print its orthology and paralogy relationships
        for ev in events:
            if ev.etype == "S":
                evts.write( ",".join(ev.in_seqs))
                evts.write("<===>")
                evts.write(",".join(ev.out_seqs))
                evts.write("\n")
            elif ev.etype == "D":
                evts.write( ",".join(ev.in_seqs))
                evts.write("<===>")
                evts.write(",".join(ev.out_seqs))
                evts.write("\n")
        evts.close()      
##########################################################################################        
#           Get support value for the evolutionary events 
##########################################################################################
        evts = file('%s''/''%s''.temp' %(events_dir,tree), "r")
        #events_and_support = file('%s''/''%s''.para.events' %(events_dir,tree), "w")
        
        output_count =0
        for row in evts:

            pair = row.split("<===>" )
            left = "".join(pair[0].split())
            right = "".join(pair[1].split())
            if (len(left) > 0 and len(right) > 0):
            	child_left = left.split(",")
            	child_right = right.split(",")
            	ancestor_1 = t.get_common_ancestor(child_left[0], child_right[0])
                #print child_left[0] + "\t" + child_right[0] 
                #print ancestor_1
                #a counter to score the number of monocots genes
                mono_left =0 
                mono_right = 0
                #para_left = 0
                #para_right= 0
                Cpent_left = 0
                Cpent_right =0
                Cpent_list = list()

                rosid_left = 0
                rosid_right=0
                asterid_left=0
                asterid_right =0 

                basal_left = 0
                basal_right =0
                ancient_left = 0
                ancient_right=0

                #####not include Vitis and Phoda which are slow evolving##############################
                ######################################################################################



                for i in child_left:
                    if i.startswith("gnl_Phypa"):   ancient_left +=1
                    if i.startswith("gnl_Selmo"):   ancient_left +=1
                    if i.startswith("gnl_Pinta"):   ancient_left +=1
                    if i.startswith("gnl_Ambtr"):   basal_left +=1
                    if i.startswith("gnl_Nelnu"):   basal_left +=1
                    if i.startswith("gnl_Aquco"):   basal_left +=1

                    if i.startswith("gnl_Vitvi"):   rosid_left +=1
                    if i.startswith("gnl_Arath"):   rosid_left +=1
                    if i.startswith("gnl_Medtr"):   rosid_left +=1
                    if i.startswith("gnl_Phavu"):   rosid_left +=1
                    if i.startswith("gnl_Prupe"):   rosid_left +=1
                    if i.startswith("gnl_Eucgr"):   rosid_left +=1
                    if i.startswith("gnl_Poptr"):   rosid_left +=1
                    if i.startswith("gnl_Theca"):   rosid_left +=1
                    if i.startswith("gnl_Carpa"):   rosid_left +=1
                    if i.startswith("gnl_Manes"):   rosid_left +=1
                    if i.startswith("Kalanchoe"):   rosid_left +=1
                    if i.startswith("Linum"):   rosid_left +=1
                    if i.startswith("Capsella"):   rosid_left +=1
                    if i.startswith("Eutrema"):   rosid_left +=1


                    if i.startswith("gnl_Betvu"):   asterid_left+=1
                    if i.startswith("Amaranthus"):  asterid_left+=1   
                    if i.startswith("gnl_kiwi"):    asterid_left+=1
                    if i.startswith("artichoke"):   asterid_left+=1   
                    if i.startswith("Daucus"):  asterid_left+=1   
                    if i.startswith("Cc_coffee"):   asterid_left+=1
                    if i.startswith("gnl_Solly"):   asterid_left+=1   
                    if i.startswith("Nicotiana"):   asterid_left+=1  
                    if i.startswith("Ipomea"):  asterid_left+=1   
                    if i.startswith("Fraxinus"):    asterid_left+=1
                    if i.startswith("gnl_Utrgi"):   asterid_left+=1
                    if i.startswith("Sesamum"): asterid_left+=1
                    if i.startswith("gnl_Mimgu"):   asterid_left+=1


                    if i.startswith("gnl_Spipo"):   mono_left +=1
                    if i.startswith("gnl_Musac"):   mono_left+=1
                    if i.startswith("gnl_Orysa"):   mono_left +=1
                    if i.startswith("gnl_Sorbi"):   mono_left +=1
                    if i.startswith("gnl_Elagu"):   mono_left +=1

                    if i.startswith("Cuscuta"):
                        Cpent_left+=1
                        Cpent_list.append(i)

                for i in child_right:
                    if i.startswith("gnl_Phypa"):   ancient_right +=1
                    if i.startswith("gnl_Selmo"):   ancient_right +=1
                    if i.startswith("gnl_Pinta"):   ancient_right +=1
                    if i.startswith("gnl_Ambtr"):   basal_right +=1
                    if i.startswith("gnl_Nelnu"):   basal_right +=1
                    if i.startswith("gnl_Aquco"):   basal_right +=1

                    if i.startswith("gnl_Vitvi"):   rosid_right +=1
                    if i.startswith("gnl_Arath"):   rosid_right +=1
                    if i.startswith("gnl_Medtr"):   rosid_right +=1
                    if i.startswith("gnl_Phavu"):   rosid_right +=1
                    if i.startswith("gnl_Prupe"):   rosid_right +=1
                    if i.startswith("gnl_Eucgr"):   rosid_right +=1
                    if i.startswith("gnl_Poptr"):   rosid_right +=1
                    if i.startswith("gnl_Theca"):   rosid_right +=1
                    if i.startswith("gnl_Carpa"):   rosid_right +=1
                    if i.startswith("gnl_Manes"):   rosid_right +=1
                    if i.startswith("Kalanchoe"):   rosid_right +=1
                    if i.startswith("Linum"):   rosid_right +=1
                    if i.startswith("Capsella"):   rosid_right +=1
                    if i.startswith("Eutrema"):   rosid_right +=1


                    if i.startswith("gnl_Betvu"):   asterid_right+=1
                    if i.startswith("Amaranthus"):  asterid_right+=1   
                    if i.startswith("gnl_kiwi"):    asterid_right+=1
                    if i.startswith("artichoke"):   asterid_right+=1   
                    if i.startswith("Daucus"):  asterid_right+=1   
                    if i.startswith("Cc_coffee"):   asterid_right+=1
                    if i.startswith("gnl_Solly"):   asterid_right+=1   
                    if i.startswith("Nicotiana"):   asterid_right+=1  
                    if i.startswith("Ipomea"):  asterid_right+=1   
                    if i.startswith("Fraxinus"):    asterid_right+=1
                    if i.startswith("gnl_Utrgi"):   asterid_right+=1
                    if i.startswith("Sesamum"): asterid_right+=1
                    if i.startswith("gnl_Mimgu"):   asterid_right+=1


                    if i.startswith("gnl_Spipo"):   mono_right +=1
                    if i.startswith("gnl_Musac"):   mono_right+=1
                    if i.startswith("gnl_Orysa"):   mono_right +=1
                    if i.startswith("gnl_Sorbi"):   mono_right +=1
                    if i.startswith("gnl_Elagu"):   mono_right +=1

                    if i.startswith("Cuscuta"):
                        Cpent_right+=1
                        Cpent_list.append(i)

  
                #the node that each row is traversing is ancestor_1
                if (rosid_left >0 and rosid_right ==0 and asterid_left ==0 and asterid_right ==0 and ancient_left ==0 and ancient_right ==0  and basal_left==0 and basal_right==0 and mono_left==0 and mono_right==0 ) or (rosid_left ==0 and rosid_right>0 and asterid_left ==0 and asterid_right ==0 and ancient_left ==0 and ancient_right ==0 and basal_left==0 and basal_right==0 and mono_left==0 and mono_right==0 )  or (rosid_left >0 and rosid_right>0 and asterid_left ==0 and asterid_right ==0 and ancient_left ==0 and ancient_right ==0 and basal_left==0 and basal_right==0 and mono_left==0 and mono_right==0 ):
 
                    if (Cpent_left >0 and Cpent_right ==0) or (Cpent_right >0 and Cpent_left ==0) or (Cpent_right >0 and Cpent_left  > 0):
                        # if the node has only 1 parasite gene
                        
                        if len(Cpent_list) ==1:
                            #print "yes"
                            node = t&Cpent_list[0]
                            node1 = node.up
                            ances_dict = dict()
                            ances_dict[1] = node1

                            interior_dict = dict()
                            interior_dict[1] = node1

                            index =1
                            have_upper_node =True
                        
                            while have_upper_node:
                                try:
                                    index = index + 1
                                    node_previous= ances_dict[index-1]
                                    ances_dict[index] =node_previous.up
                                    
                                except:
                                    have_upper_node = False

                            int_index =1
                            have_interior_node =True
                            
                            
                            while have_interior_node:
                                try:
                                    int_index = int_index + 1
                                    node_outer= interior_dict[int_index-1] 
                                    t1 = node_outer
                                    for node in t1.children:
                                        if node.is_leaf():
                                            if re.match(r"^Cuscuta",node.name):
                                                pass
                                            else:
                                                interior_dict[int_index] = node

                                        else:
                                            interior_dict[int_index] = node
                                            
                                    
                                except:
                                    have_interior_node = False

                            #bs_value_list represents the bootstrap values for interior nodes
                            if int(node1.support) >= 50:
                                #print "yes, node1 has BS value greater than 50"
                                bs_value_list = list()
                                bs_value_list.append(node1.support)

                                if node1 in ancestor_1 or node1 == ancestor_1:
                                    for i in interior_dict.keys():
                                        #print "node " + str(i) + " has nodes or interior nodes shown as below:"
                                        #print interior_dict[i]
                                        #temp_node = interior_dict[i]
                                        #print "with node support values as " + str(temp_node.support)
                                        if i>1:
                                            if interior_dict[i] is None:
                                                pass
                                            else:
                                                node = interior_dict[i]
                                                if node in ancestor_1 or node == ancestor_1:
                                                    bs_value_list.append(node.support)


                                            #################################get the left or rigt node that has more than one leaf####################################################################################################
                                            #################################get their bs value, and if node1 has bs >=50, and one of the interior node has bs >=50, then it fits model2##############################################
                                        # else:
                                        #     node = ances_dict[i]
                                        #     if node in ancestor_1 or node == ancestor_1:
                                        #         bs_value_list.append(node.support)

                                #as long as one of the bs_value_list contains node1 which is 1 strong supported node, if the inner node is stronglys supported, it fits model2
                                
                                #for bs in bs_value_list:    print bs
                                max_value = 0
                                max_value = max(bs_value_list[1:])

                                bs_count = 0
                                for bs in bs_value_list:
                                    if bs >=50:
                                        bs_count = bs_count + 1
                                if bs_count ==1:
                                    if max_value <50 and len(bs_value_list[1:]) ==1 :
                                        print "Orthogroup number: " + ortho + " has the big node shown as:"
                                        print ancestor_1
                                        print "the node1 support consisting the Cuscuta gene and rosid donor is " + str(node1.support) + " with the node shown as:"
                                        print node1

                        elif len(Cpent_list) >1:
                            Cpent_num = len(Cpent_list)
                            for Cp_i in range(0, Cpent_num):
                                #if node1 only contains Amborella genes, then node1 has to go up until it has a non-Ambtr leaf
                                node_Cp = t&Cpent_list[Cp_i]
                                Cpent_only = True
                                node1 = ""
                                current_node = node_Cp
                                while Cpent_only:
                                    node1 = current_node.up
                                    leaf_node_list = list()
                                    for temp_nod in node1.traverse("postorder"):
                                        if temp_nod.is_leaf():
                                            leaf_node_list.append(temp_nod.name)
                                    non_Cp_count = 0
                                    for leaf in leaf_node_list:
                                        if leaf.startswith("Cuscuta"):
                                            non_Cp_count += 0
                                        else:
                                            non_Cp_count += 1
                                    if non_Cp_count >=1:
                                        Cpent_only = False
                                    else:
                                        current_node = node1

                                ances_dict = dict()
                                ances_dict[1] = node1

                                interior_dict = dict()
                                interior_dict[1] = node1

                                index =1
                                have_upper_node =True
                            
                                while have_upper_node:
                                    try:
                                        index = index + 1
                                        node_previous= ances_dict[index-1]
                                        ances_dict[index] =node_previous.up
                                        
                                    except:
                                        have_upper_node = False

                                int_index =1
                                have_interior_node =True
                                
                                
                                while have_interior_node:
                                    try:
                                        int_index = int_index + 1
                                        node_outer= interior_dict[int_index-1] 
                                        t1 = node_outer
                                        for node in t1.children:
                                            if node.is_leaf():
                                                if re.match(r"^Cuscuta",node.name):
                                                    pass
                                                else:
                                                    interior_dict[int_index] = node

                                            else:
                                                interior_dict[int_index] = node
                                                
                                        
                                    except:
                                        have_interior_node = False

                                #bs_value_list represents the bootstrap values for interior nodes
                                if int(node1.support) >= 50:
                                    #print "yes, node1 has BS value greater than 50"
                                    bs_value_list = list()
                                    bs_value_list.append(node1.support)

                                    if node1 in ancestor_1 or node1 == ancestor_1:
                                        for i in interior_dict.keys():
                                            #print "node " + str(i) + " has nodes or interior nodes shown as below:"
                                            #print interior_dict[i]
                                            #temp_node = interior_dict[i]
                                            #print "with node support values as " + str(temp_node.support)
                                            if i>1:
                                                if interior_dict[i] is None:
                                                    pass
                                                else:
                                                    node = interior_dict[i]
                                                    if node in ancestor_1 or node == ancestor_1:
                                                        bs_value_list.append(node.support)


                                                #################################get the left or rigt node that has more than one leaf####################################################################################################
                                                #################################get their bs value, and if node1 has bs >=50, and one of the interior node has bs >=50, then it fits model2##############################################
                                            # else:
                                            #     node = ances_dict[i]
                                            #     if node in ancestor_1 or node == ancestor_1:
                                            #         bs_value_list.append(node.support)

                                    #as long as one of the bs_value_list contains node1 which is 1 strong supported node, if the inner node is stronglys supported, it fits model2
                                    
                                    #for bs in bs_value_list:    print bs
                                    max_value = 0
                                    try:
                                        max_value = max(bs_value_list[1:])

                                        bs_count = 0
                                        for bs in bs_value_list:
                                            if bs >=50:
                                                bs_count = bs_count + 1
                                        if bs_count ==1:
                                            if max_value <50 and len(bs_value_list[1:]) ==1 :
                                                print "Orthogroup number: " + ortho + " has the big node shown as:"
                                                print ancestor_1
                                                print "the node1 support consisting the Cuscuta gene and rosid donor is " + str(node1.support) + " with the node shown as:"
                                                print node1
                                    except:
                                        pass



                                    
        evts.close()




  