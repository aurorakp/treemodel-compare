import os
import re
import subprocess
from make_rplotscript import make_rplotscript

tree_name = "rescaledbase"

all_coords = tree_name + "_all_coords.txt"
all_coords_mn = tree_name + "_all_coords_with_mn.txt"
all_coords_mn_maj = tree_name + "_all_coords_with_mn_maj.txt"
center_tree_file = "centre_1"
# Bayes treeout:
# tree_file = tree_name + "treeout.txt"
# tree_file_mn_1st = tree_name + "_and_mean_treeout.txt"
# tree_file_mn_1st_maj_2nd = tree_name + "_and_mean_maj_treeout.txt"

tree_file = tree_name + "treeout.txt"
#tree_file = tree_name + "_raxmlout.txt"
tree_file_mn_1st = tree_name + "_and_mean_out.txt"
tree_file_mn_1st_maj_2nd = tree_name + "_and_mean_maj_out.txt"
analysis_version = "analysis_140702.jar"
sturm_version = "SturmMean_130704.jar"
mean_file_name = tree_name + "_meanfile.txt"
mean_tree_file = tree_name + "_mean.txt"
majority_file_name = tree_name + ".nex.con.tre"
majority_tree_file = tree_name + "_majority.txt"


if __name__ == '__main__':

    # To make a log map of all trees:
    if not os.path.exists(all_coords):
    
        command = 'java -jar ' + analysis_version + ' -u -a log_map -o ' + all_coords + ' -f '  + center_tree_file + " " + tree_file
        subprocess.call(command.split())
    
    # Find the mean of all trees:
    if not os.path.exists(mean_file_name):
        command = "java -jar " + sturm_version + " -a random -e 0.0001 -o " + mean_file_name + " " + tree_file
        subprocess.call(command.split())
    
    # Extract the mean tree into a file:
    # From my_helper
    
    if not os.path.exists(mean_tree_file):
        sturmMean_output_file = open(mean_file_name,'r')
        outfile = open(mean_tree_file,'w')
        for line in sturmMean_output_file:
            match_tree = re.match(r'(\(.+)',line)
            if match_tree:
                break
        sturmMean_output_file.close()
        if match_tree:
             outfile.write(match_tree.group(1) + "\n")
             outfile.close()
        else: 
            print "Warning: could not extract tree from the output file " + mean_file_name + "; returning empty string"
    
    
    # Make the tree file including the mean:
    
    if not os.path.exists(tree_file_mn_1st):
        infile1 = open(tree_file,'r')
        infile2 = open(mean_tree_file,'r')
        outfile = open(tree_file_mn_1st,'w')
        outfile.write(infile2.readline())
        for line in infile1:
            outfile.write(line)
        infile1.close()
        infile2.close()
        outfile.close()
    
    
    # Make the log map of trees + mean tree:
    
    if not os.path.exists(all_coords_mn):
        command = 'java -jar ' + analysis_version + ' -u -a log_map -o ' + all_coords_mn + ' -f '  + center_tree_file + " " + tree_file_mn_1st
        subprocess.call(command.split())
    
    # Extract the majority tree into a file:
    '''
    if not os.path.exists(majority_tree_file):
        # First, get taxa:
        infile = open(majority_file_name,'r')
        taxa = []
        tree_line = ""
        for line in infile:
            temp = line.split()
            m = re.match('[0-9]+',temp[0])   # check for the labels
            if (m):
                taxa.append(temp[1].rstrip(',;'))
            elif (temp[0] == "tree"):
                tree_line = temp[4]
                break   # once we hit the tree portion of the nexus file, we're done
        infile.close()
        
        # Then, extract newick tree from the con_tree probability string:
        tree_sub = re.sub(r'\[.*?\]',"",tree_line)
        t_with_taxa = []
        for i in range(len(taxa)+1):
            for j in xrange(1,len(taxa)+1):
                tree_sub = re.sub(str(j)+':',taxa[j-1]+':',tree_sub)
        outfile = open(majority_tree_file,'w')
        outfile.write(tree_sub)
        outfile.close()    
    '''
    # Make the tree file including the mean and majority tree:
    
    if not os.path.exists(tree_file_mn_1st):
        infile1 = open(tree_file_mn_1st, 'r')
        #infile2 = open(majority_tree_file, 'r')
        infile3 = open(tree_file,'r')
        outfile = open(tree_file_mn_1st, 'w')
        outfile.write(infile1.readline() + "\n")
        infile1.close()
        #outfile.write(infile2.readline() + "\n")
        #infile2.close()
        for line in infile3:
            outfile.write(line)
        infile3.close()
        outfile.close()
    
    # Find the coordinates for mean, majority, and all trees:
    
    if not os.path.exists(all_coords_mn):
        
        command = 'java -jar ' + analysis_version + ' -u -a log_map -o ' + all_coords_mn + ' -f '  + center_tree_file + " " + tree_file_mn_1st
        subprocess.call(command.split())
    
    # Generate the R script for the trees:
    
    # This version gets all three:
    #newbase_r = make_rplotscript(all_coords_mn_maj,"Trees with Base, Mean & Majority","log",1,True,True)
    newbase_r = make_rplotscript(all_coords_mn,"Trees with Base & Mean","log",1,True,False)
    newbase_r.set_base(1,10)
    newbase_r.rplot(True)