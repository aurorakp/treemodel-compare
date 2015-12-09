'''
Created on Jun 4, 2015

@author: alkpongsema

'''

import os
import re

class BayesExtract(object):
    '''
    This class extracts generations, likelihoods, and trees
     from a MrBayes run and places it into a two text files,
     one with all the information and another for trees only
    
    '''
    
    # default constructor
    
    def __init__(self, treeName, treefile, outpath, treeNum=50, runNum=1):
        '''
        Default constructor only takes the treeName and assumes the user wants to use
        run #1 for the basis of analysis, using 50 trees
        '''
        self.name = treefile
        self.treeNum = treeNum
        self.runNum = runNum
        self.outpath = outpath
        self.treeName = treeName
        self.tfile = treefile + "." + "run" + str(runNum) + ".t"
        self.pfile = treefile + "." + "run" + str(runNum) + ".p"
        self.outfile = outpath + "\\" + self.treeName + "out.txt"
        self.treeout = outpath + "\\" + self.treeName + "treeout.txt"
        self.treelabel = outpath + "\\" + self.treeName + "trees_labelled.txt"
    
    # Extract the point IDs and likelihoods, and match them with their trees
    
   
    def treeMatch(self):
        
        generations = []
        likelihoods = []
        trees = []
        # print "tfile is: " + self.tfile
        # print "pfile is: " + self.pfile
        # print "outfile is: " + self.outfile
        # print "treeout is: " + self.treeout
        
        # Handle the .t run file:
           
        t_length = 1
        t_file = open(self.tfile,'r')
        
        # Measure the length of the t file
        for line in t_file:
            t_length = t_length + 1
        t_file.close()
        
        
        
        # Process the t file for the desired number of trees by filling the appropriate
        # lists starting treeNum from file end, subtracting 1 for the "end;" line
        t_file = open(self.tfile,'r')
        t_start = t_length - self.treeNum -1  
        t_counter =1
        
        
        
        for line in t_file:
            if (t_counter < t_start):
                t_counter = t_counter + 1
            else:
                t_counter = t_counter + 1
                temp = line.split()
                if temp[0] != "end;" and temp[0] != "":
                    
                    trees.append(temp[4].strip())
            
        t_file.close()
        
        
        p_file = open(self.pfile,'r')
        p_length = 1
        for line in p_file:
            p_length = p_length + 1
        p_file.close()
        
        p_file = open(self.pfile,'r')
        p_start = p_length - self.treeNum
    
        p_counter = 1
        for line in p_file:
            if (p_counter < p_start):
                p_counter = p_counter + 1
            elif (p_counter >= p_start):
                p_counter = p_counter + 1
                temp = line.split()
                generations.append(temp[0].strip())
                likelihoods.append(temp[1].strip())
    
        p_file.close()
        
            
        
        
        #Write the Newick trees only to another text file with labels
        #First, extract taxa:
        
        infile = open(self.tfile,'r')
        taxa = []
        for line in infile:
            temp = line.split()
            m = re.match('[0-9]+',temp[0])   # check for the labels
            if (m):
                taxa.append(temp[1].rstrip(',;'))
            elif (temp[0] == "tree"):
                break   # once we hit the tree portion of the nexus file, we're done
        infile.close()
        #print taxa
        
        # Then, reunite taxa with trees:
        t_with_taxa = []
        for i in range(self.treeNum):
            temp = trees[i]
            for j in xrange(1,len(taxa)+1):
                temp = re.sub(str(j)+':',taxa[j-1]+':',temp)
            t_with_taxa.append(temp)
        
                    
              
        #  Write the data to one text file, formatted as:
        # generation likelihood Newicktree
        outfile = open(self.outfile,'w')
        for i in range(self.treeNum):
            outfile.write(generations[i]+" "+likelihoods[i]+" " + t_with_taxa[i] + "\n")
        outfile.close()

        
        # Write the Newick trees only to another text file
        treeout = open(self.treeout,'w')
        for i in range(self.treeNum):
            treeout.write(t_with_taxa[i]+"\n")
        treeout.close()
          
                    
                     
        

        