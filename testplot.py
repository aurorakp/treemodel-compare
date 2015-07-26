'''
Created on Jun 12, 2015

@author: alkpongsema
'''

import os
import hypothesis
import my_helper
from subprocess import call

    
if __name__ == '__main__':
    
    
    
    num_samples = 100
    num_reps = 1500
    nu = 1
    sigma = 1
    
    # code version
    sturm_version = "SturmMean_130704.jar"
    analysis_version = "analysis_140702.jar"
    
    # output files
    #Bayes
    #trees_file_name = "newbasetreeout.txt"
    #trees_topo_file_name = "newbase_tree_topo.txt"
    
    trees_file_name = "newbase_raxmlout.txt"
    trees_topo_file_name = "newbase_tree_raxmltopo.txt"
    
    '''
    # output dirs and prefixes
    sample_dir = "samples"
    means_dir = "means"
    sample_out_prefix = sample_dir + "/unif_"
    mean_file_prefix = means_dir + "/mean_unif_"
    
    
    # Generate num_reps (uniform) samples from the trees in tree_file.
    if not os.path.exists(sample_dir):
        os.mkdir(sample_dir)
        for n in xrange(num_reps):
            outfile_name = sample_out_prefix + str(n)
            hypothesis.sample_unif_from_file("basetreeout.txt",num_samples,"sample_trees.txt")
            
    else:
        print "Directory %s already exists - skipping generating tree samples \n" % sample_dir
   
           
    
    
    # Compute the mean of each sample.
    if not os.path.exists(means_dir):
        os.mkdir(means_dir)
        for n in xrange(num_reps):
            mean_file_name = mean_file_prefix + str(n)
            sample_file_name = sample_out_prefix + str(n)
            command = "java -jar " + sturm_version + " -a random -e 0.0001 -o " + mean_file_name + " " + sample_file_name
            call(command.split())
    
    else:
        print "Directory %s already exists - skipping computing means of uniform tree samples \n" % means_dir
    
    # Consolidate the means into one file.
    if not os.path.exists(trees_file_name):
        all_means_file = open(trees_file_name,'w')
        for n in xrange(num_reps):
            mean_file_name = mean_file_prefix + str(n)
            all_means_file.write(my_helper.extract_tree(mean_file_name) + '\n')
        all_means_file.close()
    
    else:
        print "File %s already exists - skipping creating file with all means \n" % trees_file_name
    
    '''
    # Get topology information about the all_means file.
    if not os.path.exists(trees_topo_file_name):
            command = "java -jar " + analysis_version + " -a topology_count -o " + trees_topo_file_name + " " + trees_file_name
            call(command.split())
    else:
        print "File %s already exists - skipping generating topology info about all means \n" % trees_topo_file_name
