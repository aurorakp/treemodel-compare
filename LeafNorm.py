'''
Created on Jul 20, 2015

@author: alkpongsema
'''
import re
import math
import os

class LeafNorm(object):
    '''
    Takes in a tree file and extracts the leaf lengths, creating a text file with the 'norm' of the leaves
    arranged in the order of the trees.
    '''


    def __init__(self, treename, treefile, treehome, model, leafNum=5):
        '''
        Constructor
        '''
        self.tree = treename
        self.treefile = treefile
        self.treehome = treehome
        self.model = model
        self.modeldir = "/" + model + "/"
        self.normfile = self.treehome + self.tree + "_" + self.model + "_norms.txt"
        self.leafNum = leafNum
        self.leafreg = ",[A-Z]:(.+?)"
        self.leafscireg = ",[A-Z]:"
        
    def setNormOut(self,normout=""):
        if (normout == ""):
            self.normfile = self.treehome + self.tree + "_" + self.model + "_norms.txt"
        else:
            self.normfile = normout
        
    def leafRegGen(self):
        leafgen = "[A-Z]:(.+?)"
        for i in range(2,self.leafNum+1):
            leafgen = leafgen + self.leafreg 
        return leafgen
        
    def findNorm(self,tree):
        '''
        Removes edges, then parentheses from tree before 
        finally extracting edge lengths from a Newick tree, then
        calculates the norm of the leaf values
        '''
        
        ### Add detection for scientific notation (or not)
        ### 
        if ("e-" in tree):
            treenoedges = re.sub(r'(\):[0-9]+[.][0-9]+[a-z]-[0-9]+)',"",tree)       
        else:
            treenoedges = re.sub(r'(\):[0-9]+[.][0-9]+)',"",tree)
            treenoedges = re.sub(r'(\):[0-9]+[.][0-9]+[A-Z][-][0-9]+)',"",treenoedges)
        treeremleftparen = re.sub(r'(\()',"",treenoedges)
        treeremrightparen = re.sub(r'(\))',"",treeremleftparen)
        treeleaves = re.match(r'.+?:(.+?),.+?:(.+?),.+?:(.+?),.+?:(.+?),.+?:(.+?);',treeremrightparen)
        leaves = treeleaves.groups()
        floatleaves = []
        for i in range(len(leaves)):
            floatleaves.append(float(leaves[i]))
        leafsumsq = 0
        for i in range(0,len(leaves)):
            leafsumsq = leafsumsq + (floatleaves[i] * floatleaves[i])
        return math.sqrt(leafsumsq)
    
    def makeNormFiles(self):
        if not os.path.exists(self.normfile):
            os.chdir(self.treehome)
            infile = open(self.treefile,'r')
            outfile = open(self.normfile,'w')
            for line in infile:
                norm = self.findNorm(line)
                outfile.write(str(norm) + "\n")
            infile.close()
            outfile.close()
        else:
            print("Norm files already created for " + self.tree + " for model " + self.model + " - skipping")
    