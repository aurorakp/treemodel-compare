'''
Created on Jul 21, 2015

@author: alkpongsema
'''
import os
import shutil
from subprocess import call
import re

class MrBayesObj(object):
    '''
    Preps, runs, and processes output for MrBayes.
    :param verbose: Given a text file with a Newick format tree, creates a directory with appropriate files, 
    including a command line script for running Mr Bayes.  Also provides tools to extract trees, likelihoods, and 
    generations from the output.
    '''


    def __init__(self, treename, basedir="C:/seqgen"):
        '''
        Constructor
        treename is the string name of the tree (no suffixes)
        basedir is the location of the tree (and place to attach directories with results)
        Note: for MrBayes, the 'best' tree is the Majority 50% rule tree in .con.tre
        '''
        self.tree = treename
        self.basedir = basedir
        self.treedir = basedir + "/"+ treename
        self.modeldir = '/bayes/'
        self.model = 'bayes'
        self.modelspc = '_bayes_'
        self.treeout = self.treedir + self.modeldir  + "/" + self.tree + "_bayes_treeout.txt"
        
    def runAll(self):
        '''
        Prepares, runs MrBayes with default parameters and treeouts.
        :param verbose: Runs MrBayes with GTR GAMMAI for 5 million generations, sampling every 1000 trees, then
        takes the last 1000 trees, the consensus tree, and creates treeouts containing just the 1000 trees, the 
        best tree also, and the likelihoods of the trees.
        '''
        self.prep()
        self.prepScript()
        self.run()
        self.rawTreeout()
        self.extractBest()
        self.bestTreeout()
        
    def runTreeouts(self):
        '''
        Only creates treeouts - one with 1000 trees and another with best tree plus 1000 trees
        '''
        self.rawTreeout()
        self.extractBest()
        self.bestTreeout()
        
    def getTreeout(self, best=False):
        if (best == True):
            return self.tree + "_bayes_best_treeout.txt"
        else:
            return self.tree + "_bayes_treeout.txt"
        
    def prep(self,textstart=True):
        # bayes_home should hold all files necessary to run MrBayes
        bayes_home = 'c:/seqgen/bayesfiles'
        bayes_dir = self.treedir + self.modeldir
        if not os.path.exists(bayes_dir):
            shutil.copytree(bayes_home, bayes_dir)
        else:
            print("Bayes files already copied for " + self.tree)
        if not os.path.exists(bayes_dir + self.tree + ".nex"):
            if (textstart==True):
                shutil.copyfile(self.basedir + "/" + self.tree + ".txt",self.treedir + self.modeldir + self.tree + ".txt")
            shutil.copyfile(self.treedir + "/" + self.tree + ".nex",self.treedir + self.modeldir + self.tree + ".nex")
        else:
            print("Tree and NEXUS files already copied for " + self.tree)
        
        
    def prepScript(self, nst=6, rates="invgamma", ngen=5000000, samplefreq=1000):
        if not os.path.exists(self.treedir + self.modeldir + self.tree + "-command.nex"):
            outfile = open(self.treedir + self.modeldir + self.tree + "-command.nex",'w')
            outfile.write("#NEXUS\n")
            outfile.write("\n")
            outfile.write("begin mrbayes;\n")
            outfile.write("\t" + "set autoclose=yes nowarn=yes;\n")
            outfile.write("\t" + "execute " + self.tree + ".nex;\n")
            outfile.write("\t" + "lset nst=" + str(nst) + " rates=" + rates + ";\n")
            outfile.write("\t" + "mcmc ngen=" + str(ngen) + " samplefreq=" + str(samplefreq) + ";\n")
            outfile.write("\t" + "sump;\n")
            outfile.write("\t" + "sumt;\n")
            outfile.write("\t" + "quit;\n")
            outfile.write("end;\n")
            outfile.close()   
        else:
            print("Skipping Mr Bayes Driver generation - already done")
            
    def run(self):
        if not os.path.exists(self.treedir + self.modeldir + self.tree + ".nex" + ".mcmc"):
            os.chdir(self.treedir + self.modeldir)
            command = "mrbayes_x64 " + self.tree + "-command.nex"
            call(command.split())
        else:
            print("Skipping Mr Bayes MCMC - already done for " + self.tree + ".")
    
    def rawTreeout(self,runNum=1,treeNum=1000):
        # Automatically takes stuff from run #1 from Mr Bayes - specify here if you want it to take
        # from a different run or if you want more/less trees extracted from the treeouts
        treefile = self.tree + ".nex"
        tfile = treefile + "." + "run" + str(runNum) + ".t"
        pfile = treefile + "." + "run" + str(runNum) + ".p"
        outfile = self.treedir + self.modeldir + "/" + self.tree + "out.txt"
        generations = []
        likelihoods = []
        trees = []
        # Process the trees 
        os.chdir(self.treedir + self.modeldir)
        t_length = 1
        t_file = open(tfile,'r')
        for line in t_file:
            t_length = t_length + 1
        t_file.close()
        t_file = open(tfile,'r')
        t_start = t_length - treeNum -1  
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
        
        # Process the likelihoods and generations
        p_file = open(pfile,'r')
        p_length = 1
        for line in p_file:
            p_length = p_length + 1
        p_file.close()
        p_file = open(pfile,'r')
        p_start = p_length - treeNum
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
        infile = open(tfile,'r')
        taxa = []
        for line in infile:
            temp = line.split()
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
        #  Write generation likelihood Newicktree
        outfile = open(outfile,'w')
        for i in range(treeNum):
            outfile.write(generations[i]+" "+likelihoods[i]+" " + t_with_taxa[i] + "\n")
        outfile.close()
    
    def extractBest(self):
        trees_best = self.tree + "_bayes_best.txt"
        trees_best_file = self.tree + ".nex.con.tre"
        os.chdir(self.treedir + self.modeldir)
        if not os.path.exists(trees_best):
            infile = open(trees_best_file,'r')
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
            for i in range(len(taxa)+1):
                for j in range(1,len(taxa)+1):
                    tree_sub = tree_sub.replace('(' + str(i) + ':','(' + taxa[i-1] + ':')
                    tree_sub = tree_sub.replace(',' + str(i) + ':',',' + taxa[i-1] + ':')
            outfile = open(trees_best,'w')
            outfile.write(tree_sub)
            outfile.close()    
        else:
            print("best tree already extracted from .con.tre for " + self.tree + "- skipping")

    def bestTreeout(self):
        os.chdir(self.treedir + self.modeldir)
        treeout = self.tree + "_bayes_treeout.txt"
        bestout = self.tree + "_bayes_best_treeout.txt"
        best = self.tree + "_bayes_best.txt"
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
            print("Bayes treeout with best tree already extracted for " + self.tree + " - skipping")
        
       