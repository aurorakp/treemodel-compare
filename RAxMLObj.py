'''
Created on Jul 21, 2015

@author: alkpongsema
'''

import os
import shutil
from subprocess import call

class RAxMLObj(object):
    '''
    Preps, runs, and processes output for RAxML.
    :param verbose: Given a text file with a Newick format tree, creates a directory with appropriate files, 
     and runs RAxML.  Also provides tools to extract trees from ouput.
    '''


    def __init__(self, treename, basedir="c:/seqgen" ):
        '''
        Constructor
        '''
        self.rax_path = "c:/raxml/"
        self.rax_ver = "raxmlHPC"
        self.raxml_dir = "/raxml"
        self.tree = treename
        self.treedir = basedir + "/" + treename
        self.model = "raxml"
        self.modeldir = "/raxml/"
        self.modelspc = "_raxml_"
        self.treeout = self.treedir + self.modeldir + self.tree + "_raxml_treeout.txt"
        
    def runAll(self):
        '''
        Prepares and runs RAxML with default parameters and treeouts.
        :param verbose: Runs RAxML with GTR, finds the 'best' tree, bootstraps 1000 trees, and creates treeouts containing 
        the bootstrap trees and one with the bootstraps and best tree also.
        '''
        self.prep()
        self.run()
        self.rawTreeout()
        self.bestTreeout()
        
    def runTreeouts(self):
        '''
        Only creates treeouts - one with 1000 trees and another with best tree plus 1000 trees
        '''
        self.rawTreeout()
        self.bestTreeout()
        
    def getTreeout(self, best=False):
        if (best == True):
            return self.tree + "_raxml_best_treeout.txt"
        else:
            return self.tree + "_raxml_treeout.txt"
       
    def prep(self):
        if not os.path.exists(self.treedir + self.tree + ".phy"):
            os.chdir(self.treedir)
            #First, convert Nexus files to Phylip format:
            command = "convbioseq phylip " +  self.tree + ".nex"
            call(command.split())
        else:
            print(self.tree + " already converted to Phylip format - skipping")
            
    def run(self,model="GTR-G"):
        if not os.path.exists(self.treedir + self.modeldir):
            # Run RAxML:
            os.mkdir(self.treedir + self.raxml_dir)
            if (model=="GTR-G"):
                os.system(self.rax_path + self.rax_ver + ' -s ' + self.treedir + '/'  + self.tree + '.phy' + ' -n ' + self.tree + ' -m GTRGAMMA -e 0.001 -f a -k -x 27362 -p 96618 -N 1000 -w ' + os.getcwd() + self.raxml_dir + "/" )
            if (model=="K80-G"):
                os.system(self.rax_path + self.rax_ver + ' -s ' + self.treedir + '/'  + self.tree + '.phy' + ' -n ' + self.tree + ' -m GTRGAMMA --K80 -e 0.1 -f a -k -x 27362 -p 96618 -N 1000 -w ' + os.getcwd() + self.raxml_dir + "/" )
        else:
            print("RAxML directory already exists for " + self.tree + " - skipping running RAxML")
            
    def rawTreeout(self):
        if not os.path.exists(self.treeout):
            os.chdir(self.treedir + self.modeldir)
            trees_file_name = self.treeout
            raxml_bootstrap = self.treedir + self.modeldir + "RAxML_bootstrap." + self.tree
            outfile = open(trees_file_name,'w')
            infile = open(raxml_bootstrap,'r')
            for line in infile:
                outfile.write(line)
            outfile.close()
            infile.close()
        else:
            print("RAxML treeout already exists for " + self.tree + " - skipping treeout creation")
            
    def bestTreeout(self):
        best_trees_file_name = self.treedir + self.modeldir + self.tree +  "_raxml_best_treeout.txt"
        if not os.path.exists(best_trees_file_name):
            os.chdir(self.treedir + self.modeldir)
            raxml_bootstrap = self.treedir + self.modeldir + "RAxML_bootstrap." + self.tree
            raxml_best = self.treedir + self.modeldir +  "RAxML_bestTree." + self.tree   
            infile1 = open(raxml_best,'r')
            infile2 = open(raxml_bootstrap,'r')
            outfile = open(best_trees_file_name,'w')
            outfile.write(infile1.readline())
            infile1.close()
            for line in infile2:
                outfile.write(line)
            infile2.close()
            outfile.close()
            outfile2 = open(self.treedir + self.modeldir + self.tree + "_raxml_best.txt",'w')
            infile3 = open(raxml_best,'r')
            for line in infile3:
                outfile2.write(line)
            outfile2.close()
            infile3.close()
           