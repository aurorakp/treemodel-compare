'''
Created on Sep 24, 2015

@author: alkpongsema
'''
import os
import shutil



if __name__ == '__main__':
    
    geneNum = 20
    basedir = "c:/seqgen/"
    os.chdir(basedir)
    models = ["bayes","BEAST","raxml","phyml"]
    for m in range(len(models)):
        modeldir = models[m] + "/"
        allmodel = "yeast_all_" + models[m] + "_treeouts.txt"
        outfile = open(allmodel,'w')    
        for i in range(1,geneNum + 1):
            yeast_string = "yeast_" + str(i) + "_genes1" 
            file_string = yeast_string + "_" + models[m] + "_treeout.txt"
            yeast_fileloc = basedir + yeast_string + "/" + modeldir + file_string
            infile = open(yeast_fileloc, 'r')
            for line in infile:
                outfile.write(line)
            infile.close()
        outfile.close()
    outfile_all = "yeast_allgenes_allmodels_treeout.txt"
    for m in range(len(models)):
        modeldir = models[m] + "/"
        outfile = open(outfile_all,'w')    
        for i in range(1,geneNum + 1):
            yeast_string = "yeast_" + str(i) + "_genes1" 
            file_string = yeast_string + "_" + models[m] + "_treeout.txt"
            yeast_fileloc = basedir + yeast_string + "/" + modeldir + file_string
            infile = open(yeast_fileloc, 'r')
            for line in infile:
                outfile.write(line)
            infile.close()
    outfile_all.close()
    # BEAST
    
    
    # PhyML
    
    
    # RAxML:
    
    
    # All:
    
      