#!/usr/bin/env python

import random
import math
import re
	
# Python module containing methods for hypothesis testing,
# includng generating distributions of trees.

#__TEST__ = False    # set this variable to 1 to get extra test output

# Methods:  random_partition_treefiles(file_name_1, file_name_2, out_file_prefix)
#           setup_generic_permutation_test(file_name_1,file_name_2,combine_func,out_file_name,permutation=None)
#           sample_unif_from_file(tree_file_name,num_samples,outfile_name)
#           sample_unif_from_2d_ball_boundary(num_samples,outfile_name)
#           sample_Gauss_around_nu_0(nu,sigma,num_samples,outfile_name)
#           sample_ex_2(nu,sigma,num_samples,outfile_name)
#           sample_ex_3(nu,sigma,num_samples,outfile_name)


#-------------------------------------------------------------------------------------

# Create two new files (out_file_prefix_1 and out_file_prefix_2) representing a random
# partition of the same size of the lines in file_name_1 union file_name_2.
# That is all lines (trees) in file_name_1 and file_name_2 appear in one of
# out_file_prefix_1 and out_file_prefix_2, which have the same number of lines
# as file_name_1 and file_name_2, respectively.
# Argument:  two files containing trees, one per line, and the output file name prefix
# Creates:  two new files containing the two new partitions.

def random_partition_treefiles(file_name_1, file_name_2, out_file_prefix):
	# read the two files into two lists
	file_1 = open(file_name_1,'r')
	trees_1 = file_1.readlines()

	file_2 = open(file_name_2,'r')
	trees_2 = file_2.readlines()

	# n = size of first partition
	n = len(trees_1)
	# m = size of second partition
	m = len(trees_2)

	# get a shuffled list
	num_list = range(n+m)
	random.shuffle(num_list)
	if __debug__:   # print out the permutation used if testing
		print 'random_partition_treefiles permutation is [%s]' % ', '.join(map(str, num_list))

	# create new files
	outfile_1 = open(out_file_prefix + '_1', 'w')
	outfile_2 = open(out_file_prefix + '_2', 'w')

	for i in xrange(n+m):
		x = num_list[i]
		if i < n:
			if x < n:
				outfile_1.write(trees_1[x])
			else:
				outfile_1.write(trees_2[x - n])
		else:
			if x < n:
				outfile_2.write(trees_1[x])
			else:
				outfile_2.write(trees_2[x - n])

# Generates set of i tests in directory test_dir, with original files
# trees_1 and trees_2, called output_prefix_0_1 and output_prefix_0_2, ....
# output_prefix_(n-1)_1 and output_prefix_(n-1)_2
#def generate_permutation_files(tree_file_1, tree_file_2, test_dir, output_prefix, n)
#	for i in range(n):
#		random_partition_treefiles(tree_file_1, tree_file_2, test_dir + '/' + output_prefix + '_i')

# Sets up a permutation test, based on combining a line from file_1
# with a line from file_2, where the lines of file_2 have been permuted.
# Outputs the result to out_file.
# Will do this for each line of first file (so second file may be bigger).
# Arguments:  file_name_1 = first file with input data
#             file_name_2 = second file with input data
#             combine_func = function for running on a line from file_1 and a
#		                     line from file_2;  output is written to out_file
#             out_file_name = file for output
		
def setup_generic_permutation_test(file_name_1,file_name_2,combine_func,out_file_name,permutation=None):
# read the two files into two lists, without newlines
	lines_1 = open(file_name_1).read().splitlines()
	lines_2 = open(file_name_2).read().splitlines()

	# n = number of lines in first file
	n = len(lines_1)
	# m = number of lines in second file
	m = len(lines_2)

	# check that n <= m  (will run n times)
	if (n>m):
		print 'Error in setup_generic_permutation_test: file %s must be at least as big as file %s' % (file_name_2,file_name_1)

	# get a shuffled list
	if (permutation == None):
		permutation = range(n)
		random.shuffle(permutation)
		if __debug__:   # print out the permutation used if testing
			print 'setup_generic_permutation_test: permutation is [%s]' % ', '.join(map(str, permutation))

	# create out files
	out_file = open(out_file_name, 'w')
	for i in xrange(n):
		out_file.write(combine_func(lines_1[i], lines_2[permutation[i]]) + '\n')
	out_file.close()

# Samples num_samples trees uniformly from the trees in tree_file_name.
# The trees in tree_file_name should be listed one per line in Newick format.
# The output is a file of trees in Newick format, one per line.
#
# Arguments: tree_file_name = name of the file to sample from
#            num_samples = number of samples
#            outfile_name = name of file to create that contains the samples
# Output: file outfile_name
	
def sample_unif_from_file(tree_file_name,num_samples,outfile_name):

	# Read in the trees (without newlines)
	trees = open(tree_file_name).read().splitlines()

	# Open the output file
	outfile = open(outfile_name, 'w')

	# Sample the trees and write to the output file.
	for n in xrange(num_samples):
		i = random.randint(0,len(trees)-1)
		outfile.write(trees[i] + '\n')

	outfile.close()

# Samples num_samples trees uniformly from the boundary of a ball of radius 1
# around the origin in T_4.  (Only interior lengths are used in the calculation.)
# The trees in tree_file_name should be listed one per line in Newick format.
# The output is a file of trees in Newick format, one per line.
#
# Arguments: num_samples = number of samples
#            outfile_name = name of file to create that contains the samples
# Output: file outfile_name

def sample_unif_from_2d_ball_boundary(num_samples,outfile_name):
        topos= ["((a:1,b:1):1,(c:1,d:1):1);",
                "((a:1,c:1):1,(b:1,d:1):1);",
                "((a:1,d:1):1,(b:1,c:1):1);",
                "(((a:1,b:1):1,c:1):1,d:1);",
                "(((a:1,b:1):1,d:1):1,c:1);",
                "(((a:1,c:1):1,b:1):1,d:1);",
                "(((a:1,c:1):1,d:1):1,b:1);",
                "(((a:1,d:1):1,b:1):1,c:1);",
                "(((a:1,d:1):1,c:1):1,b:1);",
                "(((b:1,c:1):1,a:1):1,d:1);",
                "(((b:1,c:1):1,d:1):1,a:1);",
                "(((b:1,d:1):1,a:1):1,c:1);",
                "(((b:1,d:1):1,c:1):1,a:1);",
                "(((c:1,d:1):1,a:1):1,b:1);",
                "(((c:1,d:1):1,b:1):1,a:1); "]

        # Open the output file
	outfile = open(outfile_name, 'w')

        
        # Sample the trees from topo, change the edge lengths, and write to the output file.
	for n in xrange(num_samples):
		i = random.randint(0,len(topos)-1)
                angle = random.uniform(0,math.pi/2)
                x = math.cos(angle)
                y = math.sin(angle)
                m= re.match(r'(\(.+\):)1(,.+\):)1([,\)].+)',topos[i])
                if not m:
                        print("Error:  can't change interior edges lengths in sample_unif_from_2d_ball_boundary")
                        exit
                tree = m.group(1) + str(x) + m.group(2) + str(y) + m.group(3)
                outfile.write(tree + '\n')
                        
        outfile.close()
		

# Samples num_samples trees as in Huiling's example 1.
# That is, around nu on one of the axes, sample Gaussian distribution with that as
# the center in the three adjacent orthants (with 2/3 weight), and sample
# the bottom quarter of that distribution in the 6 orthants adjacent to those (with 1/3 weight).
# The distributions have standard deviation sigma.
# The output is a file of trees in Newick format, one per line.
#
# Arguments: nu = mean of distribution
#            sigma = standard deviation of the 1-dimensional distributions
# 	  	     num_samples = number of samples
#            outfile_name = name of file to create that contains the samples
# Output: file outfile_name

def sample_gauss_around_nu_0(nu,sigma,num_samples,outfile_name):

	# Since T_4 is symmetric, we choose the axis to centre the mean on
	# arbitrarily.
    adjacent_topos= ["((a:1,b:1):1,(c:1,d:1):1);",
					 "(((a:1,b:1):1,c:1):1,d:1);",
					 "(((a:1,b:1):1,d:1):1,c:1);"]
    two_away_topos = ["(((c:1,d:1):1,a:1):1,b:1);",
		    "(((c:1,d:1):1,b:1):1,a:1);",
		    "(((b:1,d:1):1,a:1):1,c:1);",
		    "(((a:1,d:1):1,b:1):1,c:1);",
		    "(((a:1,c:1):1,b:1):1,d:1);",
                      "(((b:1,c:1):1,a:1):1,d:1);"]

        # Open the output file
    outfile = open(outfile_name, 'w')

    for n in xrange(num_samples):
        reverse_x_and_y = False
        y = abs(random.gauss(0,sigma))
        x = random.gauss(nu,sigma)

        if (x > 0):
            # Choose from adjacent_topo
            tree = adjacent_topos[random.randint(0,2)]
        else:
           # Choose from two_away_topos
           i = random.randint(0,5)
           tree = two_away_topos[i]
           if (i <2):
               reverse_x_and_y = True
           x = abs(x)

        m= re.match(r'(\(.+\):)1(,.+\):)1([,\)].+)',tree)
        if not m:
            print("Error:  can't change interior edges lengths in hypothesis.sample_gauss_around_nu_0")
            exit
        if reverse_x_and_y:
            tree = m.group(1) + str(y) + m.group(2) + str(x) + m.group(3)
        else:
            tree = m.group(1) + str(x) + m.group(2) + str(y) + m.group(3)
        outfile.write(tree + '\n')
    outfile.close()


# Samples num_samples trees as in Huiling's example 2.
# That is, around nu on one of the axes, sample Gaussian distribution with that as
# the center in the three adjacent orthants, and 6 orthants that are on the other side
# of the adjacent orthants.  However, one adjacent orthant (and corresponding two-away orthants)
# is weighted 1/2, compared to 1/4 for the others.
# The distributions have standard deviation sigma.
# The output is a file of trees in Newick format, one per line.
#
# Arguments: nu = mean of distribution
#            sigma = standard deviation of the 1-dimensional distributions
# 	     num_samples = number of samples
#            outfile_name = name of file to create that contains the samples
# Output: file outfile_name

def sample_ex_2(nu,sigma,num_samples,outfile_name):

	# Since T_4 is symmetric, we choose the axis to centre the mean on
	# arbitrarily.
    adjacent_topos= ["((a:1,b:1):1,(c:1,d:1):1);",
					 "(((a:1,b:1):1,c:1):1,d:1);",
					 "(((a:1,b:1):1,d:1):1,c:1);"]
    two_away_topos = ["(((c:1,d:1):1,a:1):1,b:1);",
		    "(((c:1,d:1):1,b:1):1,a:1);",
		    "(((b:1,d:1):1,a:1):1,c:1);",
		    "(((a:1,d:1):1,b:1):1,c:1);",
		    "(((a:1,c:1):1,b:1):1,d:1);",
                      "(((b:1,c:1):1,a:1):1,d:1);"]

        # Open the output file
    outfile = open(outfile_name, 'w')

    for n in xrange(num_samples):
        reverse_x_and_y = False
        y = abs(random.gauss(0,sigma))
        x = random.gauss(nu,sigma)

        if (x > 0):
            # Choose adjacent_topo:
            # 0 or 1: choose topo 1
            # 2: choose topo 2
            # 3: choose topo 3
            i = random.randint(0,3)
            if (i == 0 or i == 1):
                tree = adjacent_topos[0]
            elif (i == 2):
                tree = adjacent_topos[1]
            else:
                tree = adjacent_topos[2]
        else:
           x = abs(x)
           # Choose from two_away_topos
           # 1 or 2:  choose topo 0 and reverse x and y
           # 3 or 4:  choose topo 1 and reverse x and y
           # 5: choose topo 2
           # 6: choose topo 3
           # 7: choose topo 4
           # 8: choose topo 5
           i = random.randint(1,8)
           if (i ==1 or i ==2):
              tree = two_away_topos[0]
              reverse_x_and_y = True
           elif (i == 3 or i ==4):
              tree = two_away_topos[1]
              reverse_x_and_y = True
           elif (i == 5):
              tree = two_away_topos[2]
           elif (i == 6):
              tree = two_away_topos[3]
           elif (i == 7):
              tree = two_away_topos[4]
           else:
              tree = two_away_topos[5]
              
        m= re.match(r'(\(.+\):)1(,.+\):)1([,\)].+)',tree)
        if not m:
            print("Error:  can't change interior edges lengths in hypothesis.sample_gauss_around_nu_0")
            exit
        if reverse_x_and_y:
            tree = m.group(1) + str(y) + m.group(2) + str(x) + m.group(3)
        else:
            tree = m.group(1) + str(x) + m.group(2) + str(y) + m.group(3)
        outfile.write(tree + '\n')
    outfile.close()


# Samples num_samples trees as in Huiling's example 3.
# That is, around nu on one of the axes, sample either: a 2D Gaussian distribution with that as
# the center in two of the adjacent orthants, and the 4 orthants adjacent to those;
# or sample a 1D Gaussian distribution on that axis, or the 2 axes "adjacent" to it.
# The distributions have standard deviation sigma.
# The output is a file of trees in Newick format, one per line.
#
# Arguments: nu = mean of distribution
#            sigma = standard deviation of the 1-dimensional distributions
# 	     num_samples = number of samples
#            outfile_name = name of file to create that contains the samples
# Output: file outfile_name

def sample_ex_3(nu,sigma,num_samples,outfile_name):

	# Since T_4 is symmetric, we choose the axis to centre the mean on
	# arbitrarily.
    adjacent_topos= ["(((a:1,b:1):1,c:1):1,d:1);",
		     "(((a:1,b:1):1,d:1):1,c:1);"]
    two_away_topos = ["(((b:1,d:1):1,a:1):1,c:1);",
		    "(((a:1,d:1):1,b:1):1,c:1);",
		    "(((a:1,c:1):1,b:1):1,d:1);",
                      "(((b:1,c:1):1,a:1):1,d:1);"]
    p_topo = "((a:1,b:1):1,c:1,d:1);"
    two_away_1d_topos = ["((a:1,c:1,d:1):1,b:1);",
                        "((b:1,c:1,d:1):1,a:1);"]
    

        # Open the output file
    outfile = open(outfile_name, 'w')

    for n in xrange(num_samples):
        y = abs(random.gauss(0,sigma))
        x = random.gauss(nu,sigma)

        # choose either 1 or 2d distribution
        i = random.randint(1,2)
        if (i == 1):
            if (x > 0):
                # then the sampled point uses the p topology
                tree = p_topo
            else:
                # then we draw again to figure out which two_away_1d_topos we use
                j = random.randint(0,1)
                tree = two_away_1d_topos[j]
            m= re.match(r'(\(.+\):)1(.+)',tree)
            if not m:
                print("Error:  can't change interior edges lengths in hypothesis.sample_ex_3")
                exit
            tree = m.group(1) + str(abs(x)) + m.group(2)
                
        else:   # 2D case
            if (x > 0):
                # Choose adjacent_topo
                j = random.randint(0,1)
                tree = adjacent_topos[j]
            else:
                # Choose two_away_topos
                j = random.randint(0,3)
                tree = two_away_topos[j]
 
            m= re.match(r'(\(.+\):)1(,.+\):)1([,\)].+)',tree)
            if not m:
                print("Error:  can't change interior edges lengths in hypothesis.sample_ex_3")
                exit
            tree = m.group(1) + str(abs(x)) + m.group(2) + str(y) + m.group(3)
        outfile.write(tree + '\n')
    outfile.close()
