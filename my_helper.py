#!/usr/bin/env python

import re
import filecmp
import math

# Python module that contains methods for extracting data from text files.

# Methods:  extract_std_dev(file_name)  
#           extract_tree(file_name)      
#           get_diss_matrix(geo_file_name,diss_file_name,sym_flag)
#                                      sym_flag = "symmetric" or "non"
#           replace_leaves(tree, nexus_file_name)
#           extract_star_std_devs(file_name)
#           extract_tree_nexus(nexus_file_name,tree_num)
#           add_edge_lengths(tree, length)
#           extract_num_splits(file_name)
#           extract_num_topos(file_name)
#           compute_sos_variance(geo_file_name)
#           extract_iter_trees(file_name,var_outfile_name,tree_outfile_name)
#           *** not tested yet ***  extract_topos(tree_file_name,topo_file_name,out_dir_name)
#           max_dist(geo_file_name)
#           avg_dist(geo_file_name)



# Extract the standard deviation from the output of SturmMean.jar.
# Argument:  output file from SturnMean.jar
# Returns: The extracted standard deviation or an empty string.

def extract_std_dev(file_name):
    sturmMean_output_file = open(file_name,'r')
    for line in sturmMean_output_file:
        # If the line is "Standard Deviation if tree is mean: 0.098786",
        # extract the standard deviation
        match_std_dev = re.match(r'Standard Deviation if tree is mean: ([0-9\.]+)',line)
        if match_std_dev:
            break
    sturmMean_output_file.close()
    if match_std_dev:
         return match_std_dev.group(1)
    else: 
        print "Warning: could not extract the standard deviation from the output file " + file_name + "; returning empty string"
    return ""

# Extract the tree from the output of SturmMean.jar
# Argument:  output file from SturmMean.jar
# Returns: The extracted tree as a string or an empty string.

def extract_tree(file_name):
    sturmMean_output_file = open(file_name,'r')
    for line in sturmMean_output_file:
        match_tree = re.match(r'(\(.+)',line)
        if match_tree:
            break
    sturmMean_output_file.close()
    if match_tree:
        return match_tree.group(1)
    else: 
        print "Warning: could not extract tree from the output file " + file_name + "; returning empty string"
    return ""

# Extracts all star tree std devs from the file file_name,
# which should be the output of running sturmMean.
# Argument:  console output (piped to file) from SturmMean.jar
def extract_star_std_devs(file_name):
    star_std_devs = []
    console_output_file = open(file_name,'r')
    for line in console_output_file:
        match_std_dev = re.match(r'Standard deviation if star tree is mean: ([0-9\.]+)',line)
        if match_std_dev:
            star_std_devs.append(match_std_dev.group(1))
    console_output_file.close()
    return star_std_devs

   

# Reads in the raw output of GTP (or the two file version)
# and creates a dissimilarity matrix file of the distances.
# Arguments: raw distance file output from GTP
#            output file
#            "symmetric" or "non" : whether matrix should be symmetric or not
# Returns:  nothing (writes to output file)
def get_diss_matrix(geo_file_name,diss_file_name,sym_flag):
    max_row = 0
    max_col = 0

    # Loop through the geo file the first time to get the dimensions
    # of diss_matrix
    geo_dist_file = open(geo_file_name,'r')
    for line in geo_dist_file:
        match_line = re.match(r'([0-9]+)\s([0-9]+)\s([0-9\.E-]+)',line)
        if (match_line):
            if ( int(match_line.group(1)) > max_row):
                max_row = int(match_line.group(1))
            if ( int(match_line.group(2)) > max_col):
                max_col = int(match_line.group(2))
    geo_dist_file.close()

    # Create and populate the diss_matrix
    geo_dist_file = open(geo_file_name,'r')

	# add one to max_row if symmetric matrix
	# (because last row is not output by GTP because determined by symmetry)
    if (sym_flag == "symmetric"):
        max_row= max_row + 1
        if (max_row != max_col):
            print "Error:  symmetric matrix but read in %d rows and %d columns.  Exiting" % (max_row + 1, max_col +1)
            exit(1)

    # add one because rows/cols were labelled 0, 1, 2, ... by GTP
    diss_matrix = [ [0]*(max_col+1) for x in xrange(max_row+1)]

    # Loop through the geo file the second time to populate diss_matrix
    for line in geo_dist_file:
        match_line = re.match(r'([0-9]+)\s([0-9]+)\s([0-9\.E-]+)',line)

        if (match_line):
            diss_matrix[int(match_line.group(1))][int(match_line.group(2))]	= match_line.group(3)
            if (sym_flag == "symmetric"):
                diss_matrix[int(match_line.group(2))][int(match_line.group(1))]	= match_line.group(3)

    geo_dist_file.close()

	# print the geodesic distances as a dissimilarity matrix to the output file.
    o = open(diss_file_name,'w')

    for row in range(max_row + 1):
        for col in range(max_col + 1):
            o.write(str(diss_matrix[row][col]) + ' ')
        o.write('\n')
    o.close()

# Replace the leaves in a Newick tree with the translations given in a Nexus file.
# Arguments:  string containing the Newick tree
#             string containing the Nexus file name
# Returns: string containing the Newick tree with the leaves replaced as specified by the Nexus file

def replace_leaves(tree, nexus_file_name):
    # get leaf map from Nexus file and store in dictionary nexus_map
    # key is the number, value is the actual leaf name
    nexus_map = dict()

    nexus_file = open(nexus_file_name,'r')
    for line in nexus_file:
        match_translate = re.match(r'\s+(\d+) (\w+)[;,]',line)
        if match_translate:
            nexus_map[match_translate.group(1)] = match_translate.group(2)
            # print('number is ' + match_translate.group(1) + ' and species is ' + match_translate.group(2))
    nexus_file.close()

    # a leaf is the number between ( or, and :
    # or if there are no edge lengths, between ( and ,
	# or between , and )

    new_tree = ""
	#  match_leaf = re.match(r'^(.*?[\(,])(\d+):(.+)',tree)
    match_leaf = re.match(r'^(.*?[\(,])(\d+)([:,\)].+)',tree)
    while match_leaf:
        new_tree = new_tree + match_leaf.group(1) + nexus_map[match_leaf.group(2)]
        tree = match_leaf.group(3)
        match_leaf = re.match(r'^(.*?[\(,])(\d+)([:,\)].+)',tree)
    new_tree = new_tree + tree
    return new_tree



# Returns the tree at position tree_num in a Nexus file, with the leaves translated.
# Arguments:  string containing Nexus file name
#             positive integer containing the tree number that we want to extract.
#                  The first tree is 1, etc.
# Returns:  string containing the Newick tree, with the leaves translated

def extract_tree_nexus(nexus_file_name,tree_num):
    tree_counter = 0

    in_file = open(nexus_file_name,'r')
    line = in_file.readline()
    while line:
        match_tree = re.match(r'^\s+tree.*?(\(.*?;)',line)
        if match_tree:
            # if we have a tree, increment the tree_counter
            tree_counter += 1
            if (tree_counter == tree_num):
                # save tree
                tree = match_tree.group(1)
                break;
        line = in_file.readline()

    # translate the leave of the tree
    translated_tree = replace_leaves(tree,nexus_file_name)
    return translated_tree

# Adds edge lengths of 1 to a tree input in Newick format (without edge lengths)
# Arguments:  tree = tree without edge lengths in Newick format
#             length = length to set all the edges to
# Returns:  tree in Newick format with all edges having specified length
def add_edge_lengths(tree, length):
	# edge lengths should go before , and )
	tree = tree.replace(',',':' + str(length) + ',')
	tree = tree.replace(')',':' + str(length) + ')')
	return tree

# Extracts the number of distinct splits found by analysis.jar -a split_count
# Arguments:  file_name = file output by analysis.jar -a split_count
# Returns: # of distinct splits found as an integer
def extract_num_splits(file_name):
	split_file = open(file_name,'r')

	for line in split_file:
		match = re.match(r'Raw split counts:  (.*)',line)
		if match:
			split_freq_list = match.group(1).split(' ')
			return len(split_freq_list)
	return -1

# Extracts the number of distinct topologies found by analysis.jar -a topology_count
# Arguments:  file_name = file output by analysis.jar -a topology_count
# Returns: # of distinct topologies found as an integer
def extract_num_topos(file_name):
	topo_file = open(file_name,'r')

	for line in topo_file:
		match = re.match(r'Raw topology counts:  (.*)',line)
		if match:
			topo_freq_list = match.group(1).split(' ')
			return len(topo_freq_list)
	return -1

# Computes the variance defined as the sum of the squares of all inter-tree distances.
# Assumes that each (non-empty) line in the input file contains a distance that
# we want to use for the computation (i.e. that there are no duplicates).
# Arguments: file_name = a raw distance file output by gtp.jar or distances.jar
# Returns:  computed variance
def compute_sos_variance(geo_file_name):
	variance = 0.0

	# loop through the file to get the distances
	geo_dist_file = open(geo_file_name,'r')
	for line in geo_dist_file:
		match_line = re.match(r'([0-9]+)\s([0-9]+)\s([0-9\.]+)',line)
		if (match_line):
			dist = float(match_line.group(3))
			variance = variance + math.pow(dist,2)
	geo_dist_file.close()
	
	return variance

# From the screen output produced by SturmMean when run with the iteration flag,
# extract the variances and trees, writing them in the same order, one per line,
# in the file var_outfile_name or tree_outfile_name, respectively.
# Arguments:  file_name = piped screen output of SturmMean -i
#             var_outfile_name = writes just the intermediate variances to this file
#             tree_outfile_name = writes just the intermediate trees to this file
# Returns: nothing

def extract_iter_info(file_name,var_outfile_name,tree_outfile_name):
    in_file = open(file_name,'r')
    var_outfile = open(var_outfile_name,'w')
    tree_outfile = open(tree_outfile_name,'w')

    for line in in_file:
         match_line = re.match(r'Iteration [0-9]+\. Variance, tree: ([0-9\.]+), (\(.+)',line)
         if (match_line):
            var_outfile.write(match_line.group(1) + '\n')
            tree_outfile.write(match_line.group(2) + '\n')

    var_outfile.close()
    tree_outfile.close()
    in_file.close()

# Divides the trees in tree_file_name up by topology.
# The trees of each topology are written to a new file in directory out_dir_name.
# Arguments: tree_file_name = file containing original tree
#            topo_file_name = file output by running analysis.jar -a topology_counts
#                               on tree_file_name
#            out_dir_name = directory topology files are written to
#
# Returns: nothing
# Creates: one file ("topo_i") for each unique topology containing all trees of that topology

def extract_topos(tree_file_name,topo_file_name,out_dir_name):
    topo_file = open(topo_file_name,'r')
    tree_file = open(tree_file_name,'r')

    flag = 0
    topos = []
    for line in topo_file:
        if (flag == 1):
            match = re.match(r'(\d*)',line)
            topo_num = match.group(1)
            # write the next tree to topology file
            tree = tree_file.readline()
            out_file = open("topo_" + topo_num,'a')
            out_file.write(tree)
            out_file.close()
            
        else:
            match = re.match(r'Raw topology counts:',line)
            if match:
                flag = 1

# Computes the max distance of the distances in geo_file_name.
#
# Arguments:  File of raw geodesic distances
#
# Returns: Maximum distance in the input file.
                
def max_dist(geo_file_name):
    max = 0.0

    geodist_file = open(geo_file_name,'r')
    for line in geodist_file:
        match_line = re.match(r'[0-9]+\s[0-9]+\s([0-9\.E-]+)',line)

        if (match_line):
            dist = match_line.group(1)
            if (float(dist) > float(max)):
                max = dist
    return max

# Computes the average distance of the distances in geo_file_name.
#
# Arguments:  File of raw geodesic distances
#
# Returns: Average distance in the input file.
                
def avg_dist(geo_file_name):
    avg = 0.0
    count = 0

    geodist_file = open(geo_file_name,'r')
    for line in geodist_file:
        match_line = re.match(r'[0-9]+\s[0-9]+\s([0-9\.E-]+)',line)

        if (match_line):
            dist = match_line.group(1)
            avg = avg + float(dist)
            count = count + 1
    return avg/count

