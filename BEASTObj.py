'''
Created on Jul 21, 2015

@author: alkpongsema
'''
import os
import shutil
from subprocess import call
import re
from time import sleep

class BEASTObj(object):
    '''
    Requires TreeAnnotator and BEAST: partially preps, runs, and processes output for BEAST.
    :param verbose: Given a text file with a Newick format tree, prepares directories and files for BEAUti,
    runs BEAST, and prepares treeouts for BEAST output.  Needs updating to run BEAUti from command line if that becomes
    possible.
    
    '''


    def __init__(self, treename, basedir="c:/seqgen"):
        '''
        Note: for BEAST, the 'best' tree is the one created by using the associated program TreeAnnotator
        '''
        self.tree = treename
        self.basedir = basedir
        self.treedir = self.basedir + "/" + self.tree
        self.model = "BEAST"
        self.modeldir = "/BEAST/"
        self.modelspc = "_BEAST_"
        self.treeout = self.treedir + self.modeldir + self.tree + "_BEAST_treeout.txt"
        
    def runAll(self):
        '''
        Requires BEAUti to be run first to convert nexus files to BEAST format
        '''
        self.prep()
        self.run()
        self.rawTreeout()
        self.findBest()
        self.bestTreeout()
        
   
    def runTreeouts(self):
        '''
        Only creates treeouts - one with 1000 trees and another with best tree plus 1000 trees
        '''
        self.rawTreeout()
        self.findBest()
        self.bestTreeout()
    
    def getTreeout(self, best=False):
        if (best == True):
            return self.tree + "_BEAST_best_treeout.txt"
        else:
            return self.tree + "_BEAST_treeout.txt"
    
    def prep(self):
        '''
        Assumes BEAST xml format files are in base tree directory
        '''
        if not os.path.exists(self.treedir + self.modeldir):
            os.chdir(self.treedir)
            os.mkdir(self.treedir + self.modeldir)
            shutil.copy(self.treedir + "/" +  self.tree + ".nex", self.treedir + self.modeldir + self.tree + ".nex")
            shutil.copy(self.treedir + "/" +  self.tree  + ".xml", self.treedir + self.modeldir  + self.tree + ".xml")
            shutil.copy(self.treedir + "/" +  self.tree  + "_state.xml", self.treedir + self.modeldir  + self.tree + "_state.xml")
        else:
            print("BEAST directory already exists - skipping post BEAUti prep for " + self.tree)
    
    def run(self):
        '''
        Assumes BEAST jar is installed in beast_path
        '''
        beast_path = "c:/BEAST/lib/"
        beast_ver = "beast.jar"
        beast_rawout = self.tree + ".trees"
        beauti_out = self.tree + ".xml"
        state_file = self.tree + "_state.xml"
    
        if not os.path.exists(self.treedir + self.modeldir + beast_rawout):
            os.chdir(self.treedir + self.modeldir)
            os.system("java -jar " + beast_path + beast_ver + " -beagle -working -seed 777 -statefile " + state_file + " " + beauti_out)
        else:
            print("BEAST directory already exists - skipping running BEAST")
            
    def rawTreeout(self,treeNum=1000):
        if not os.path.exists(self.treeout):
            os.chdir(self.treedir + self.modeldir)
            trees = []
            self.tfile = self.tree + ".trees"
            # Handle the .t run file:
            t_length = 1
            t_file = open(self.tfile,'r')
            for line in t_file:
                t_length = t_length + 1
            t_file.close()
            t_file = open(self.tfile,'r')
            t_start = t_length - treeNum -1  
            t_counter =1
            for line in t_file:
                if (t_counter < t_start):
                    t_counter = t_counter + 1
                else:
                    t_counter = t_counter + 1
                    temp = line.split()
                    if (temp[0] != "End;" and temp[0] != ""):
                        trees.append(temp[3].strip())
            t_file.close()
            
            #Write the Newick trees only to another text file with labels
            infile = open(self.tfile,'r')
            taxa = []
            for line in infile:
                temp = line.split()
                if (len(temp) == 0):
                    continue
                else:
                    m = re.match('[0-9]+',temp[0])   # check for the labels
                    if (m):
                        taxa.append(temp[1].rstrip(',;'))
                    elif (temp[0] == "tree"):
                        break   # once we hit the tree portion of the nexus file, we're done
            infile.close()
            t_with_taxa = []
            for i in range(treeNum):
                temp = trees[i]
                for j in range(1,len(taxa)+1):
                    temp = temp.replace('(' + str(j) + ':','(' + taxa[j-1] + ':')
                    temp = temp.replace(',' + str(j) + ':',',' + taxa[j-1] + ':')
                t_with_taxa.append(temp)
            treeout = open(self.treeout,'w')
            for i in range(treeNum):
                treeout.write(t_with_taxa[i]+"\n")
            treeout.close()
            
           

                
        else:
            print("Beast treeout already extracted from " + self.tree + ".trees - skipping")
        
    def findBest(self):
        '''
        Uses Tree Annotator to find the best tree from BEAST output
        '''

        beast_path = "c:/BEAST/"
        treeanno_ver = "treeannotator"
        beast_best = self.tree + "_best"
        burnin = 25
        
        if not os.path.exists(self.treedir + self.modeldir + beast_best):
            
            command =  beast_path + treeanno_ver + " -burnin " + str(burnin) + " " + self.treedir + self.modeldir + self.tree + ".trees " +  self.treedir + self.modeldir + beast_best 
            print command
            call(command.split())
            # Added sleep command as subprocess.call does not play well with TreeAnnotator and I need
            # to be sure that TreeAnnotator finishes before proceeding 
            sleep(5)
                
           
        else:
            print("Tree Annotator already run for " + self.tree + " - skipping")
        
        os.chdir(self.treedir + self.modeldir)    
        trees_best = self.tree + "_BEAST_best.txt"
        trees_best_file = beast_best
        if not os.path.exists(trees_best):
            # First, get taxa:
            infile = open(trees_best_file,'r')
            taxa = []
            tree_line = ""
            for line in infile:
                temp = line.split()
                if (len(temp) == 0):
                    continue
                else:
                    m = re.match('[0-9]+',temp[0])   # check for the labels
                    if (m):
                        taxa.append(temp[1].rstrip(',;'))
                    elif (temp[0] == "tree"):
                        tree_line = temp[3]
                        break   # once we hit the tree portion of the nexus file, we're done
            infile.close()
            
            # Then, extract newick tree from the con_tree probability string:
            tree_sub = re.sub(r'\[.*?\]',"",tree_line)
            for i in range(1,len(taxa)+1):
                tree_sub = tree_sub.replace('(' + str(i) + ':','(' + taxa[i-1] + ':')
                tree_sub = tree_sub.replace(',' + str(i) + ':',',' + taxa[i-1] + ':')
            outfile = open(trees_best,'w')
            outfile.write(tree_sub)
            outfile.close()    
        else:
            print("Best tree already extracted from " + self.tree + ".trees - skipping")
    
    def bestTreeout(self):
        os.chdir(self.treedir + self.modeldir)
        treeout = self.tree + "_BEAST_treeout.txt"
        bestout = self.tree + "_BEAST_best_treeout.txt"
        best = self.tree + "_BEAST_best.txt"
        if not os.path.exists(bestout):
            infile2 = open(best, 'r')
            infile3 = open(treeout, 'r')
            outfile = open(bestout, 'w')
            outfile.write(infile2.readline() + "\n")
            infile2.close()
            for line in infile3:
                outfile.write(line)
            infile3.close()
            outfile.close()
        else:
            print("Beast treeout with best tree already extracted for " + self.tree + " - skipping")
        