'''
Created on Aug 2, 2015

@author: alkpongsema
'''
from jarutils import countTopos
import os
import re

class TopoManip(object):
    '''
    classdocs
    '''


    def __init__(self, treelist, modellist = ["bayes","raxml","phyml"], treefilesuff = ["_bayes_treeout.txt","_raxml_treeout.txt","_phyml_treeout.txt"], runNum=2, basedir="c:/seqgen"):
        '''
        Constructor
        '''
        self.basedir = basedir
        self.treelist = treelist
        self.modellist = modellist
        self.treefilesuff = treefilesuff
        self.runNum = runNum
        self.outprefix = self.setOutPrefix()
        self.topooutprefix = self.setTopoOutPrefix()
    
    
    '''
    need to make a printout/chart with
    topos, names, model names, etc.
    and also the topologies (small versions)
    '''
    
    def setTopoOutPrefix(self, topooutprefix = "yeastgenes"):
        self.topooutprefix = topooutprefix
        
    def setOutPrefix(self,outprefix="yeastgenes"):
        self.outprefix = outprefix    
        
    def makeheadersuff(self, sims=1):
        headsuff = ""
        for i in range(len(self.modellist)):
            if (sims == 1):
                headsuff = headsuff + self.modellist[i] + ","
            else:
                headsuff = headsuff + self.modellist[i] + ","
                for j in range(sims):
                    headsuff = headsuff + self.modellist[i] + "_" + str(j) + "," 
        headsuff.rstrip(",")
        headsuff = headsuff + "\n"
        return headsuff
    
    def countToposOut(self):
        ## Counts topologies found for each type of simulation
        for j in range(1,self.runNum + 1):
            os.chdir(self.basedir)
            outfile = open(self.topooutprefix + str(j) + ".txt",'w')
            header = "tree," + self.makeheadersuff()
            outfile.write(header)
            for i in range(len(self.treelist)):
                treek = self.treelist[i] + str(j)
                treeline = treek
               
                for m in range(len(self.modellist)):
                    treedir = self.basedir + "/" + treek + "/" + self.modellist[m] + "/"
                    topofile = treek + "_" + self.modellist[m] + "_tree_topo.txt"
                    treeline = treeline + "," + str(countTopos(topofile,treedir))
                outfile.write(treeline + "\n")
            outfile.close()
            
    def countToposTwoModsOut(self, treelist2,headerlist2):
        ## Counts topologies for two different base trees (i.e. two models)
        for j in range(1,self.runNum + 1):
            os.chdir(self.basedir)
            outfile = open("treeleafgrowstopotable" + str(j) + ".txt",'w')
            header = "tree," + self.makeheadersuff(2)
            outfile.write(header)
            for i in range(len(self.treelist)):
                treek = self.treelist[i] + str(j)
                treeg = treelist2[i] + str(j) 
                treeline = treek
               
                for m in range(len(self.modellist)):
                    treedir = self.basedir + "/" + treek + "/" + self.modellist[m] + "/"
                    topofile = treek + "_" + self.modellist[m] + "_tree_topo.txt"
                    treeline = treeline + "," + str(countTopos(topofile,treedir))
                    topofile = treeg + "_" + self.modellist[m] + "_tree_topo.txt"
                    treeline = treeline + "," + str(countTopos(topofile,treedir))
                outfile.write(treeline + "\n")
            outfile.close()
            
    def listTopos(self):
        ## Outputs a file with the tree topologies in the file listed
        for j in range(1,self.runNum+1):
            os.chdir(self.basedir)
            outfile = open(self.outprefix +  "_" + str(j) + "_topolist.txt",'w')
            for i in range(len(self.treelist)):
                treek = self.treelist[i] + str(j)
                outfile.write(treek + "\n")
                treeline = ""
                
                for m in range(len(self.modellist)):
                    treedir = self.basedir + "/" + treek + "/" + self.modellist[m] + "/"
                    topofile = treek + "_" + self.modellist[m] + "_tree_topo.txt"
                    topoCount = countTopos(topofile, treedir)
                    topoline = ""
                    # Parse topology file:
                    tfile = open(treedir + topofile,'r')
                    for line in tfile:
                        temp = line.split()
                        if (re.search(r'([0-9][.])',temp[0]) != None):
                            topoline = topoline + temp[1] + ","
                        elif (temp[0] == "Raw"):
                            topoline = self.modellist[m] + "," + topoline
                            break
                        else:
                            continue
                    outfile.write(treeline + topoline.rstrip(",") + "\n")
            outfile.close()    
    
    def masterList(self):
        header = "tree model topo treespertopo"
        
        
    def listEachTopo(self):
        for j in range(1,self.runNum+1):
            os.chdir(self.basedir)
            for i in range(len(self.treelist)):
                treek = self.treelist[i] + str(j)
                outfile = open(treek + "_" + "treespertopo.txt",'w')
                for m in range(len(self.modellist)):
                    treedir = self.basedir + "/" + treek + "/" + self.modellist[m] + "/"
                    topofile = treek + "_" + self.modellist[m] + "_tree_topo.txt"
                    treeline = self.modellist[m] + " "
                    infile = open(treedir + topofile,'r')
                    rawflag = False
                    for line in infile:
                        temp = line.split()
                        if (temp[0] == "Raw"):
                            treeline = treeline + line.lstrip("Raw topology counts:  ")
                            outfile.write(treeline)
                            rawflag = True
                        if (rawflag == True):
                            break
                    infile.close()
                outfile.close()