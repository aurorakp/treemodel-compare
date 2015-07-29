'''
Created on Jul 22, 2015

@author: alkpongsema
'''
import shutil
import os
from MrBayesObj import MrBayesObj
from RAxMLObj import RAxMLObj
from BEASTObj import BEASTObj
from PhyMLObj import PhyMLObj
from jarutils import *
from LeafNorm import LeafNorm
from LogMapPlotter import LogMapPlotter

if __name__ == '__main__':
    tree = "hillisunrooted"
    basedir = "c:/seqgen"
    runNum = 2
    '''
    tree = "seagrass"
    basedir = "c:/seqgen"
    
    for i in range(1,11):
        treePhyML = PhyMLObj(tree + str(i))
        treePhyML.prep()
        treePhyML.run(model="K80-G")
    
    tree = "largeleaves"
    models = ["bayes","raxml","BEAST","phyml"]
    for i in range(1,11):
            for m in range(len(models)):
                model_dir = "/" + models[m] + "/"
                treehome = basedir + "/" + tree + str(i) + model_dir    
                treefiles = [tree + str(i) + "_bayes_treeout.txt",tree + str(i) + "_raxml_treeout.txt",tree + str(i) + "_BEAST_treeout.txt",tree + str(i) + "_phyml_treeout.txt"]
                os.chdir(treehome)
                ln = LeafNorm(tree + str(i), treefiles[m], treehome, models[m])
                ln.makeNormFiles()
                coords_dir = "coords/"
                for coords_file_name in os.listdir(coords_dir):
                    topo_dir = "split_by_topology/"
                    topo_file_name = "topo" + coords_file_name[7:]
                    cl = LeafNorm(tree + str(i), treehome + topo_dir + topo_file_name, coords_dir, models[m])
                    cl.setNormOut(treehome + coords_dir + coords_file_name[:-4] + "_norms.txt")
                    cl.makeNormFiles()
    '''                
    # 3. .jar processing and LeafNorms
    models = ["bayes","raxml"]
    
    # Generate mean tree, distance files, and distance matrices:
    
    for i in range(1,runNum):
        for m in range(len(models)):
            model_dir = "/" + models[m] + "/"
            treehome = basedir + "/" + tree + str(i) + model_dir
            #treefiles = [tree + str(i) + "_bayes_treeout.txt",tree + str(i) + "_raxml_treeout.txt",tree + str(i) + "_BEAST_treeout.txt",tree + str(i) + "_phyml_treeout.txt"]
            treefiles = [tree + str(i) + "_bayes_treeout.txt",tree + str(i) + "_raxml_treeout.txt"]
            copyjars(treehome)
            if (models[m] == "BEAST"):
                findSturmMean(tree + str(i), treehome, models[m], rooted=True)
                geoDistanceMatrix(tree + str(i), treefiles[m], treehome, models[m], distlabel = "", rooted=True)
            else:
                findSturmMean(tree + str(i), treehome, models[m], rooted=False)
                geoDistanceMatrix(tree + str(i), treefiles[m], treehome, models[m], distlabel = "", rooted=False)
            if not os.path.exists(treehome + tree + str(i) + "_" + models[m] + "_norms.txt"):
                ln = LeafNorm(tree + str(i), treefiles[m], treehome, models[m])
                ln.makeNormFiles()
        
    # 4. Coordinate discovery for logmaps
    #models = ["bayes","raxml","phyml"]
    models = ["bayes","raxml"]
    #models = ["BEAST"]
    for i in range(1,runNum+1):
        for m in range(len(models)):
            model_dir = "/" + models[m] + "/"
            treehome = basedir + "/" + tree + str(i) + model_dir
            treefiles = [tree + str(i) + "_bayes_treeout.txt",tree + str(i) + "_raxml_treeout.txt"]
            #treefiles = [tree + str(i) + "_BEAST_treeout.txt"]
            #treefiles = [tree + str(i) + "_raxml_treeout.txt",tree + str(i) + "_BEAST_treeout.txt",tree + str(i) + "_phyml_treeout.txt"]
            logplot = LogMapPlotter(tree + str(i), treefiles[m], treehome, models[m], rooted=True)
            logplot.split_topos()
            logplot.make_centres()
            logplot.make_coords()
            
            #logplot.plot_coords_all()
            #logplot.plot_coords_quads()
            # To delete directories and their contents:
            #shutil.rmtree(treehome + "quadrant_plots")
            #orderByLogMap(tree + str(i), basedir + "/" + tree + str(i), models[m], best=False, orderby=1, bynorm=False)
            #orderByLogMap(tree + str(i), basedir + "/" + tree + str(i), models[m], best=False, orderby=1, bynorm=True)