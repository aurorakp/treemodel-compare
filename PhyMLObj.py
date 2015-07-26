'''
Created on Jul 21, 2015

@author: alkpongsema
'''

import os
import shutil
from subprocess import call
import re

class PhyMLObj(object):
    '''
    Requires convbioseq utility!  Preps, runs, and processes output for PhyML.
    :param verbose: Given a text file with a Newick format tree, creates a directory with appropriate files using
    convbioseq and runs PhyML.  Also provides tools to extract trees from ouput.
    '''


    def __init__(self, treename, basedir="c:/seqgen"):
        '''
        Constructor
        '''
        self.tree = treename
        self.basedir = basedir
        self.treedir = self.basedir + "/" + self.tree
        self.model = "phyml"
        self.modeldir = "/phyml/"
        self.modelspc = "_phyml_"
        self.treeout = self.treedir + self.modeldir + self.tree + "_phyml_treeout.txt"
    
    
    def runAll(self):
        '''
        Prepares and runs PhyML with default parameters and treeouts.
        :param verbose: Runs PhyML with GTR-Gamma-I equivalency, finds the 'best' tree, bootstraps 1000 trees, and creates treeouts containing 
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
            return self.tree + "_phyml_best_treeout.txt"
        else:
            return self.tree + "_phyml_treeout.txt"
    
    def prep(self):
        if not os.path.exists(self.treedir + self.tree + ".phy"):
            os.chdir(self.treedir)
            #First, convert Nexus files to Phylip format:
            command = "convbioseq phylip " +  self.tree + ".nex"
            call(command.split())
        else:
            print(self.tree + " already converted to Phylip format - skipping")
    
    def run(self,model="GTR-G"):
        phyml_path = "c:/phyml/bin/"
        phyml_ver = "phyml"
               
        if not os.path.exists(self.treedir + self.modeldir):
            #Run PhyML:
            os.mkdir(self.treedir + self.modeldir)
            shutil.copy(self.treedir + "/" + self.tree + ".phy", self.treedir + "/" + self.modeldir + self.tree + ".phy")
            os.chdir(self.treedir + self.modeldir)
            if (model=="GTR-G"):
                os.system(phyml_path + phyml_ver + ' -i ' + self.tree + ".phy -b 1000 -c 4 -a e -m GTR -v e")
            if (model=="K80-G"):
                print("command is: " + phyml_path + phyml_ver + ' -i ' + self.tree + ".phy -b 1000 -c 4 -a e -m K80 -v e" )
                os.system(phyml_path + phyml_ver + ' -i ' + self.tree + ".phy -b 1000 -c 4 -a e -m K80 -v e")
        else:
            print("PhyML directory already exists - skipping running PhyML")
        
    def rawTreeout(self):
        if not os.path.exists(self.treeout):
            os.chdir(self.treedir + self.modeldir)
            trees_file_name = self.treeout
            phyml_bootstrap = self.treedir + self.modeldir + self.tree + ".phy_phyml_boot_trees.txt"
            outfile = open(trees_file_name,'w')
            infile = open(phyml_bootstrap,'r')
            for line in infile:
                outfile.write(line)
            outfile.close()
            infile.close()
        else:
            print("PhyML treeout already exists - skipping extraction for " + self.tree)
    
    def bestTreeout(self):
        os.chdir(self.treedir + self.modeldir)
        infile1 = open(self.tree + ".phy" + "_phyml_tree.txt",'r')
        best_tree = re.sub(r'([0-9]+:)',":",infile1.readline())
        infile2 = open(self.tree + ".phy" + "_phyml_boot_trees.txt",'r')
        outfile = open(self.tree + "_phyml_best_treeout.txt",'w')
        outfile.write(best_tree)
        infile1.close()
        for line in infile2:
            outfile.write(line)
        infile2.close()
        outfile.close()
        outfile2 = open(self.tree + "_phyml_best.txt",'w')
        outfile2.write(best_tree)
        outfile2.close()
        