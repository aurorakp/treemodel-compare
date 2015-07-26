'''
Created on Jun 24, 2015

@author: alkpongsema
'''
import re
import subprocess
import os

class distrib_compare(object):
    '''
    Takes two files of trees:
    1) Finds the mean tree of each
    2) Computes the distances between the mean tree and each tree in the tree file
    3) Creates an R plot script to compare the relative means and distances for each
    '''


    def __init__(self, treefile1, treefile2, mean_jar = "SturmMean_130704.jar", analysis_jar ="analysis_140702.jar"):
        '''
        Constructor
        Condition: treefile1 and treefile2 must be two distinct files
        '''
        tree_file_1 = treefile1
        tree_file_2 = treefile2
        tree_mean_1 = re.sub(r'([.].+)',"",treefile1) + "_mean.txt"
        tree_mean_2 = re.sub(r'([.].+)',"",treefile2) + "_mean.txt"
        dist_to_mean_1 = re.sub(r'([.].+)',"",treefile1) + "_dist.txt"
        dist_to_mean_2 = re.sub(r'([.].+)',"",treefile2) + "_dist.txt"
        if (treefile1 == treefile2):
            raise Exception("Must input tree files with different names.")
        sturm_version = mean_jar
        analysis_version = analysis_jar
    
    
    def find_means(self):
        #if not os.path.exists(self.tree_mean_1):
            command = "java -jar " + self.sturm_version + " -a random -e 0.0001 -o " + self.tree_mean_1 + " " + self.tree_file_1
            subprocess.call(command.split())
        #else:
        #    print "Skipping mean creation for tree 1 - already done"
        #if not os.path.exists(self.tree_mean_2):
            command = "java -jar " + self.sturm_version + " -a random -e 0.0001 -o " + self.tree_mean_2 + " " + self.tree_file_2
            subprocess.call(command.split())
        #else:
        #   print "Skipping mean creation for tree 2 - already done"
            
    def find_disttomean(self):
        if not os.path.exists(self.dist_to_mean_1):
            command = 'java -jar ' + self.analysis_version + ' -u -a gtp_twofiles -o ' + self.dist_to_mean_1 + ' -f '  + self.tree_file_1 + " " + self.tree_mean_1
            subprocess.call(command.split())
        else:
            print "Skipping distances to mean for tree 1 - already done"
        if not os.path.exists(self.dist_to_mean_2):
            command = 'java -jar ' + self.analysis_version + ' -u -a gtp_twofiles -o ' + self.dist_to_mean_2 + ' -f '  + self.tree_file_2 + " " + self.tree_mean_2
            subprocess.call(command.split())
        else:
            print "Skipping distances to mean for tree 2 - already done"
    #def plot_qq(self):
        
     