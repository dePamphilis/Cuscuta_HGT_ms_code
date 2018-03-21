#!/usr/bin/python
##########################################################################################
#
# Program to scan newick phylogenetic tree and get duplication events among orobanchaceae
# (Triphysaria, Striga, Orobanche, and Lindenbergia) and support values usng species 
# overlap (SO) algorithm.
# No other outgroups can be on either side of the duplication node. Lindenbergia must be
# present on at least one side. Any two of Triphysaria, Striga, and Orobanche can
# be missing on each side, but at least one taxon must be present on both sides.
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
	from ete2 import PhyloTree
	from ete2 import Tree
	print >>sys.stdout, "printing to stdout during suppression"
	print >>sys.stderr, "printing to stderr during suppression"
		 
print >>sys.stdout, "printing to stdout after suppression"
print >>sys.stderr, "printing to stderr after suppression"

# check for user input - tree directory
if (len(sys.argv) != 2 ):
	print "get_HGT_from_cuscuta2rosids_v3.3.4.5.py <newick_trees_dir>"
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
#           evolutionary events involving all taxa
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
				Cpent_left = 0
				Cpent_right= 0
				rosid_left = 0
				rosid_right=0
				asterid_left=0
				asterid_right =0 
				other_left = 0
				other_right =0
				#para_list = list()
				rosid_list = list()

				#soft_para_left = 0
				#soft_para_right=0
				Cpent_list = list()

				for i in child_left:
					if i.startswith("gnl_Phypa"):   other_left +=1
					if i.startswith("gnl_Selmo"):   other_left +=1
					if i.startswith("gnl_Pinta"):   other_left +=1
					if i.startswith("gnl_Ambtr"):   other_left +=1
					if i.startswith("gnl_Nelnu"):   other_left +=1
					if i.startswith("gnl_Aquco"):   other_left +=1
					if i.startswith("gnl_Arath"):
						rosid_left +=1
						rosid_list.append(i)

					if i.startswith("gnl_Eucgr"):
						rosid_left+=1
						rosid_list.append(i)
					if i.startswith("gnl_Carpa"):
						rosid_left +=1
						rosid_list.append(i)
					if i.startswith("gnl_Theca"):
						rosid_left +=1
						rosid_list.append(i)
					if i.startswith("gnl_Poptr"):
						rosid_left +=1
						rosid_list.append(i)
					if i.startswith("gnl_Manes"):
						rosid_left +=1
						rosid_list.append(i)
					if i.startswith("Kalanchoe"):
						rosid_left +=1
						rosid_list.append(i)
					if i.startswith("Linum"):
						rosid_left +=1
						rosid_list.append(i)
					if i.startswith("Capsella"):
						rosid_left +=1
						rosid_list.append(i)
					if i.startswith("Eutrema"):
						rosid_left +=1
						rosid_list.append(i)
					if i.startswith("gnl_Prupe"):
						rosid_left +=1
						rosid_list.append(i)
					if i.startswith("gnl_Phavu"):
						rosid_left +=1
						rosid_list.append(i)
					if i.startswith("gnl_Medtr"):
						rosid_left+=1
						rosid_list.append(i)
					if i.startswith("gnl_Vitvi"):
						rosid_left +=1
						rosid_list.append(i)
					if i.startswith("gnl_Solly"):   asterid_left+=1
					if i.startswith("gnl_Betvu"):   asterid_left +=1
					if i.startswith("Amaranthus"):  asterid_left+=1  
					if i.startswith("gnl_Utrgi"):   asterid_left +=1
					if i.startswith("gnl_kiwi"):    asterid_left+=1
					if i.startswith("artichoke"):   asterid_left+=1   
					if i.startswith("Daucus"):  asterid_left+=1   
					if i.startswith("Cc_coffee"):   asterid_left+=1
					if i.startswith("Nicotiana"):   asterid_left+=1  
					if i.startswith("Ipomea"):  asterid_left+=1   
					if i.startswith("Fraxinus"):    asterid_left+=1
					if i.startswith("gnl_Utrgi"):   asterid_left+=1
					if i.startswith("Sesamum"): asterid_left+=1
					if i.startswith("gnl_Mimgu"):
						asterid_left+=1
						#soft_para_left +=1


					# if i.startswith("gnl_Stras"):
					#   para_left+=1
					#   soft_para_left +=1
					#   para_list.append(i)
					if i.startswith("gnl_Spipo"):   mono_left +=1
					if i.startswith("gnl_Orysa"):   mono_left +=1
					if i.startswith("gnl_Elagu"):   mono_left+=1
					if i.startswith("gnl_Sorbi"):   mono_left +=1
					if i.startswith("gnl_Musac"):   mono_left+=1

					if i.startswith("Cpent"):
						Cpent_left+=1
						Cpent_list.append(i)


				for i in child_right:
					if i.startswith("gnl_Phypa"):   other_right +=1
					if i.startswith("gnl_Selmo"):   other_right +=1
					if i.startswith("gnl_Pinta"):   other_right +=1
					if i.startswith("gnl_Ambtr"):   other_right +=1
					if i.startswith("gnl_Nelnu"):   other_right +=1
					if i.startswith("gnl_Aquco"):   other_right +=1
					
					if i.startswith("gnl_Arath"):
						rosid_right +=1
						rosid_list.append(i)
					if i.startswith("gnl_Eucgr"):
						rosid_right+=1
						rosid_list.append(i)
					if i.startswith("gnl_Carpa"):
						rosid_right +=1
						rosid_list.append(i)
					if i.startswith("gnl_Theca"):
						rosid_right +=1
						rosid_list.append(i)
					if i.startswith("gnl_Poptr"):
						rosid_right +=1
						rosid_list.append(i)
					if i.startswith("gnl_Manes"):
						rosid_right +=1
						rosid_list.append(i)
					if i.startswith("Kalanchoe"):
						rosid_right +=1
						rosid_list.append(i)
					if i.startswith("Linum"):
						rosid_right +=1
						rosid_list.append(i)
					if i.startswith("Capsella"):
						rosid_right +=1
						rosid_list.append(i)
					if i.startswith("Eutrema"):
						rosid_right +=1
						rosid_list.append(i)
					if i.startswith("gnl_Prupe"):
						rosid_right +=1
						rosid_list.append(i)
					if i.startswith("gnl_Phavu"):
						rosid_right +=1
						rosid_list.append(i)
					if i.startswith("gnl_Medtr"):
						rosid_right+=1
						rosid_list.append(i)
					if i.startswith("gnl_Vitvi"):
						rosid_right +=1
						rosid_list.append(i)
					if i.startswith("gnl_Solly"):   asterid_right+=1
					if i.startswith("gnl_Betvu"):   asterid_right +=1
					if i.startswith("Amaranthus"):  asterid_right+=1  
					if i.startswith("gnl_Utrgi"):   asterid_right +=1
					if i.startswith("gnl_kiwi"):    asterid_right+=1
					if i.startswith("artichoke"):   asterid_right+=1   
					if i.startswith("Daucus"):  asterid_right+=1   
					if i.startswith("Cc_coffee"):   asterid_right+=1
					if i.startswith("Nicotiana"):   asterid_right+=1  
					if i.startswith("Ipomea"):  asterid_right+=1   
					if i.startswith("Fraxinus"):    asterid_right+=1
					if i.startswith("gnl_Utrgi"):   asterid_right+=1
					if i.startswith("Sesamum"): asterid_right+=1
					if i.startswith("gnl_Mimgu"):
						asterid_right+=1
						#soft_para_left +=1


					# if i.startswith("gnl_Stras"):
					#   para_left+=1
					#   soft_para_left +=1
					#   para_list.append(i)
					if i.startswith("gnl_Spipo"):   mono_right +=1
					if i.startswith("gnl_Orysa"):   mono_right +=1
					if i.startswith("gnl_Elagu"):   mono_right+=1
					if i.startswith("gnl_Sorbi"):   mono_right +=1
					if i.startswith("gnl_Musac"):   mono_right+=1

					if i.startswith("Cpent"):
						Cpent_right+=1
						Cpent_list.append(i)

				
				#we used soft_para because sometimes the monophylytic group of the parasites can contain Lindenbergia or Mimulus
				if (Cpent_left >0 and Cpent_right >0 and asterid_left ==0 and asterid_right ==0 and mono_left ==0 and mono_right ==0 and other_left==0 and other_right==0) or (Cpent_left >0 and Cpent_right ==0 and asterid_left ==0 and asterid_right ==0 and mono_left ==0 and mono_right ==0 and other_left==0 and other_right==0) or (Cpent_left ==0 and Cpent_right >0 and asterid_left ==0 and asterid_right ==0 and mono_left ==0 and mono_right ==0 and other_left==0 and other_right==0):
					#print "yes"
					
					#now we must require that the parasite genes are present - so look at the clade that must have parasite genes in
					if len(Cpent_list) >=1:
						#now we screen for if rosids are grouped within the parasitic plants
						if len(rosid_list) >=1:
							# if the node has only 1 rosid gene
							# if len(rosid_list) ==1:
							#     #print "yes"
							#     node = t&rosid_list[0]
							#     node1 = node.up
							#     ances_dict = dict()
							#     ances_dict[1] = node1
							#     index =1
							#     have_upper_node =True
							
							#     while have_upper_node:
							#         try:
							#             index = index + 1
							#             node_previous= ances_dict[index-1]
							#             ances_dict[index] =node_previous.up
										
							#         except:
							#             have_upper_node = False

							#     if int(node1.support) >= 50:
							#         bs_value_list = list()

							#         for i in ances_dict.keys():
							#             if i >1:
							#                 if ances_dict[i] is None:
							#                     pass
							#                 else:
							#                     node = ances_dict[i]
							#                     if node in ancestor_1 or node == ancestor_1:
							#                         bs_value_list.append(node.support)

							#         #as long as one of the bs_value_list(which has already excluded the node1) is greater than 50, then it is a puative HGT event
							#         bs_count = 0
							#         for bs in bs_value_list:
							#             if bs >=50:
							#                 bs_count = bs_count + 1
							#             if bs_count >=1:
							#                 output_count = output_count + 1
							#                 if output_count == 1:
							#                     print "Orthogroup number: " + ortho + " has the big node shown as:"
							#                     print ancestor_1
							#                     print "the node1 support consisting the parasite gene and the rosid donor is " + str(node1.support) + " with the node shown as:"
							#                     print node1

							#                     node2 = ""
							#                     max_value = max(bs_value_list)
							#                     node2 = ""
							#                     #print str(max_value)
							#                     for i in ances_dict.keys():
							#                         if i >1:
							#                             if ances_dict[i] is None:
							#                                 pass
							#                             else:
							#                                 node = ances_dict[i]
							#                                 if node in ancestor_1 or node == ancestor_1:
							#                                     if node.support == max_value:
							#                                         #print node
							#                                         node2 = node
							#                     print "the 2nd highly supported node consisting the parasite gene and the rosid donor is " + str(node2.support) + " with the node shown as:"
							#                     print node2
							if len(rosid_list) ==3:
								#print "yes"
								#node = t.get_common_ancestor(rosid_list[0],rosid_list[1])
								node = t.get_common_ancestor(rosid_list[0],rosid_list[1],rosid_list[2])
								#print node
								have_upper_node =True
								while have_upper_node:
									try:
										node1 = node.up
										ances_dict = dict()
										ances_dict[1] = node1
										index =1
										have_upper_node =True
									
										while have_upper_node:
											try:
												index = index + 1
												node_previous= ances_dict[index-1]
												ances_dict[index] =node_previous.up
												
											except:
												have_upper_node = False

										if int(node1.support) >= 50:
											#print "yes"
											bs_value_list = list()

											for i in ances_dict.keys():
												if i >1:
													if ances_dict[i] is None:
														pass
													else:
														node = ances_dict[i]
														#print node
														if node in ancestor_1 or node == ancestor_1:
															#print "yes"
															bs_value_list.append(node.support)

											#as long as one of the bs_value_list(which has already excluded the node1) is greater than 50, then it is a puative HGT event
											bs_count = 0

											for bs in bs_value_list:
												if bs >=50:
													bs_count = bs_count + 1
												if bs_count >=1:
													output_count = output_count + 1
													if output_count == 1:
														print "Orthogroup number: " + ortho + " has the big node shown as:"
														print ancestor_1
														print "the node1 support consisting the parasite gene and the rosid donor is " + str(node1.support) + " with the node shown as:"
														print node1

														node2 = ""
														max_value = max(bs_value_list)
														node2 = ""
														#print str(max_value)
														for i in ances_dict.keys():
															if i >1:
																if ances_dict[i] is None:
																	pass
																else:
																	node = ances_dict[i]
																	if node in ancestor_1 or node == ancestor_1:
																		if node.support == max_value:
																			#print node
																			node2 = node
														print "the 2nd highly supported node consisting the parasite gene and the rosid donor is " + str(node2.support) + " with the node shown as:"
														print node2

									except:
										have_upper_node = False
							elif len(rosid_list) ==4:
								#print "yes"
								#node = t.get_common_ancestor(rosid_list[0],rosid_list[1])
								node = t.get_common_ancestor(rosid_list[0],rosid_list[1],rosid_list[2],rosid_list[3])
								#print node
								have_upper_node =True
								while have_upper_node:
									try:
										node1 = node.up
										ances_dict = dict()
										ances_dict[1] = node1
										index =1
										have_upper_node =True
									
										while have_upper_node:
											try:
												index = index + 1
												node_previous= ances_dict[index-1]
												ances_dict[index] =node_previous.up
												
											except:
												have_upper_node = False

										if int(node1.support) >= 50:
											#print "yes"
											bs_value_list = list()

											for i in ances_dict.keys():
												if i >1:
													if ances_dict[i] is None:
														pass
													else:
														node = ances_dict[i]
														#print node
														if node in ancestor_1 or node == ancestor_1:
															#print "yes"
															bs_value_list.append(node.support)

											#as long as one of the bs_value_list(which has already excluded the node1) is greater than 50, then it is a puative HGT event
											bs_count = 0

											for bs in bs_value_list:
												if bs >=50:
													bs_count = bs_count + 1
												if bs_count >=1:
													output_count = output_count + 1
													if output_count == 1:
														print "Orthogroup number: " + ortho + " has the big node shown as:"
														print ancestor_1
														print "the node1 support consisting the parasite gene and the rosid donor is " + str(node1.support) + " with the node shown as:"
														print node1

														node2 = ""
														max_value = max(bs_value_list)
														node2 = ""
														#print str(max_value)
														for i in ances_dict.keys():
															if i >1:
																if ances_dict[i] is None:
																	pass
																else:
																	node = ances_dict[i]
																	if node in ancestor_1 or node == ancestor_1:
																		if node.support == max_value:
																			#print node
																			node2 = node
														print "the 2nd highly supported node consisting the parasite gene and the rosid donor is " + str(node2.support) + " with the node shown as:"
														print node2

									except:
										have_upper_node = False

							elif len(rosid_list) ==5:
								#print "yes"
								#node = t.get_common_ancestor(rosid_list[0],rosid_list[1])
								node = t.get_common_ancestor(rosid_list[0],rosid_list[1],rosid_list[2],rosid_list[3],rosid_list[4])
								#print node
								have_upper_node =True
								while have_upper_node:
									try:
										node1 = node.up
										ances_dict = dict()
										ances_dict[1] = node1
										index =1
										have_upper_node =True
									
										while have_upper_node:
											try:
												index = index + 1
												node_previous= ances_dict[index-1]
												ances_dict[index] =node_previous.up
												
											except:
												have_upper_node = False

										if int(node1.support) >= 50:
											#print "yes"
											bs_value_list = list()

											for i in ances_dict.keys():
												if i >1:
													if ances_dict[i] is None:
														pass
													else:
														node = ances_dict[i]
														#print node
														if node in ancestor_1 or node == ancestor_1:
															#print "yes"
															bs_value_list.append(node.support)

											#as long as one of the bs_value_list(which has already excluded the node1) is greater than 50, then it is a puative HGT event
											bs_count = 0

											for bs in bs_value_list:
												if bs >=50:
													bs_count = bs_count + 1
												if bs_count >=1:
													output_count = output_count + 1
													if output_count == 1:
														print "Orthogroup number: " + ortho + " has the big node shown as:"
														print ancestor_1
														print "the node1 support consisting the parasite gene and the rosid donor is " + str(node1.support) + " with the node shown as:"
														print node1

														node2 = ""
														max_value = max(bs_value_list)
														node2 = ""
														#print str(max_value)
														for i in ances_dict.keys():
															if i >1:
																if ances_dict[i] is None:
																	pass
																else:
																	node = ances_dict[i]
																	if node in ancestor_1 or node == ancestor_1:
																		if node.support == max_value:
																			#print node
																			node2 = node
														print "the 2nd highly supported node consisting the parasite gene and the rosid donor is " + str(node2.support) + " with the node shown as:"
														print node2

									except:
										have_upper_node = False


								
							


		evts.close()




  