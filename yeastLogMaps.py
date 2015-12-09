'''
Created on Oct 13, 2015

@author: alkpongsema
'''
import os

from subprocess import call
import shutil
from LogMapPlotter import LogMapPlotter

if __name__ == '__main__':
    
    ###  Setting up yeast logmaps to work with the 'desired' center, even if it isn't the 
    ### dominant topology.
    
    ## First, I'm zipping up the old topos/coords/quadplots:
    
    basedir = "c:/seqgen"
    yeastset = []
    runNum = 1
    for i in range(1,21):
        yeaststr = "yeast_" + str(i) + "_genes" + str(runNum)

        yeastset.append(yeaststr)
        
    models = ["bayes","raxml","BEAST","phyml"]
    
    for j in range(1,len(yeastset)):
        tree = yeastset[j]
        for m in range(len(models)):
            model_dir = "/" + models[m] + "/"
            treehome = basedir + "/" + tree + model_dir
            os.chdir(treehome)
            archiveName = tree + "_" + models[m] + ".7z"
            print "treehome is: " + treehome
            print "archiveName is: " + archiveName
            #zipUp(archiveName
            if not os.path.exists(archiveName):
                command = "C:\\Program Files\\7-Zip\\7zG.exe a -t7z " + archiveName + " centres/ coords/ quadrant_plots/ split_by_topology/"
                call(command.split())
    
    ## Now that the old files are archived, delete the old directories:
            
    for j in range(1,len(yeastset)):
        tree = yeastset[j]
        for m in range(len(models)):
            model_dir = "/" + models[m] + "/"
            treehome = basedir + "/" + tree + model_dir
            os.chdir(treehome)
            dirlist = ["centres","coords","quadrant_plots","split_by_topology"]
            for d in range(len(dirlist)):
                if os.path.exists(treehome + "/" + dirlist[d]):
                    shutil.rmtree(treehome + "/" + dirlist[d], ignore_errors=True)
                    
    
    ## Then, retrieve the values for the topology matches to ensure that we get
    ## plots based on the 'dominant' topology:
    
    topoPicked = 1   ## We want the 'dominant' topology at 20 genes.
                      ## Later, we should look at 'earlier' genes.
    
    topo_data_dir = "c:/seqgen/yeasttopodata"
    
       
    for i in range(1,len(yeastset)):
        tree = yeastset[i]
        treefiles = [tree + "_bayes_treeout.txt",tree + "_raxml_treeout.txt",tree + "_BEAST_treeout.txt",tree  + "_phyml_treeout.txt"]
                
        for m in range(len(models)):
            topo_data_file = topo_data_dir + "/yeast_" + models[m] + "_" + str(topoPicked) + "_topomatches.txt"
            treehome = basedir + "/" + yeastset[i] + "/" + models[m] + "/"
            infile = open(topo_data_file,'r')
            sameTop = 1
            for line in infile:
                temp = line.split()
                if (temp[0] == "'" + str(i) + "'"):
                    if (temp[1] == "TRUE"):
                        sameTop = 1
                        break
                    elif (temp[2] == "TRUE"):
                        sameTop = 2
                        break
            
            logplot = LogMapPlotter(tree, treefiles[m], treehome, models[m], rooted=False)
            logplot.split_topos()
            logplot.make_centres(sameTop)
            logplot.make_coords(sameTop)
            #os.remove(tree + str(i) + "_" + models[m] + "_allcoords.r")
            #os.remove(tree + str(i) + "_" + models[m] + "_allcoords_norm3D.r")
            logplot.plot_coords_all()
            logplot.plot_coords_quads()
    
    # Next step: figure out edges for a 'progression' in topologies
             
            