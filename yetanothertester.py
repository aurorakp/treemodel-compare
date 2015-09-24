'''
Created on Aug 11, 2015

@author: alkpongsema
'''
from TopoManip import TopoManip
from jarutils import *
from LeafNorm import LeafNorm
from LogMapPlotter import LogMapPlotter

if __name__ == '__main__':
    
    basedir = "c:/seqgen"
    yeastset = []
    runNum = 1
    for i in range(1,21):
        yeaststr = "yeast_" + str(i) + "_genes"

        yeastset.append(yeaststr)
    '''    
    for i in range(len(yeastset)):
        tree = yeastset[i]
# 3. .jar processing and LeafNorms
            #models = ["bayes","raxml","BEAST","phyml"]
        models = ["bayes","raxml","BEAST","phyml"]
            # Generate mean tree, distance files, and distance matrices:
        
        
        for i in range(1,runNum+1):
            for m in range(len(models)):
                model_dir = "/" + models[m] + "/"
                treehome = basedir + "/" + tree + str(i) + model_dir
                #treefiles = [tree + str(i) + "_bayes_treeout.txt",tree + str(i) + "_raxml_treeout.txt",tree + str(i) + "_phyml_treeout.txt"]
                treefiles = [tree + str(i) + "_bayes_treeout.txt",tree + str(i) + "_raxml_treeout.txt",tree + str(i) + "_BEAST_treeout.txt",tree + str(i) + "_phyml_treeout.txt"]
                copyjars(treehome)
                if (models[m] == "BEAST"):
                    findSturmMean(tree + str(i), treehome, models[m], rooted=True)
                    geoDistanceMatrix(tree + str(i), treefiles[m], treehome, models[m], distlabel = "", rooted=True)
                else:
                    findSturmMean(tree + str(i), treehome, models[m], rooted=False)
                    geoDistanceMatrix(tree + str(i), treefiles[m], treehome, models[m], distlabel = "", rooted=False)
                #if not os.path.exists(treehome + tree + str(i) + "_" + models[m] + "_norms.txt"):
                    #ln = LeafNorm(tree + str(i), treefiles[m], treehome, models[m])
                    #ln.makeNormFiles()
            
        # 4. Coordinate discovery for logmaps
        models = ["bayes","raxml","BEAST","phyml"]
        #models = ["bayes"]
        #models = ["BEAST"]
        for i in range(1,runNum+1):
            for m in range(len(models)):
                model_dir = "/" + models[m] + "/"
                treehome = basedir + "/" + tree + str(i) + model_dir
                #treefiles = [tree + str(i) + "_bayes_treeout.txt",tree + str(i) + "_raxml_treeout.txt",tree + str(i) + "_phyml_treeout.txt"]
                #treefiles = [tree + str(i) + "_BEAST_treeout.txt"]
                treefiles = [tree + str(i) + "_bayes_treeout.txt",tree + str(i) + "_raxml_treeout.txt",tree + str(i) + "_BEAST_treeout.txt",tree + str(i) + "_phyml_treeout.txt"]
                
    
                if (models[m] == "BEAST"):
                    
                    
                    logplot = LogMapPlotter(tree + str(i), treefiles[m], treehome, models[m], rooted=True)
                    logplot.split_topos()
                    logplot.make_centres()
                    #logplot.make_coords()
                    #os.remove(tree + str(i) + "_" + models[m] + "_allcoords.r")
                    #os.remove(tree + str(i) + "_" + models[m] + "_allcoords_norm3D.r")
                    #logplot.plot_coords_all()
                    #logplot.plot_coords_quads()
                
        
                if (models[m] != "BEAST"):
                    logplot = LogMapPlotter(tree + str(i), treefiles[m], treehome, models[m], rooted=False)
                    logplot.split_topos()
                    logplot.make_centres()
                    logplot.make_coords()
                    #os.remove(tree + str(i) + "_" + models[m] + "_allcoords.r")
                    #os.remove(tree + str(i) + "_" + models[m] + "_allcoords_norm3D.r")
                    logplot.plot_coords_all()
                    logplot.plot_coords_quads()
                    # To delete directories and their contents:
                #shutil.rmtree(treehome + "quadrant_plots")
                #orderByLogMap(tree + str(i), basedir + "/" + tree + str(i), models[m], best=False, orderby=1, bynorm=False)
                #orderByLogMap(tree + str(i), basedir + "/" + tree + str(i), models[m], best=False, orderby=1, bynorm=True)
             
    '''  
    #yeastSetNum = []
    #for j in range(1,runNum+1):
    #    for k in range(len(yeastset)):
    #        yeastSetNum.append(yeastset[k] + str(j))
    models = ["bayes","raxml","BEAST","phyml"]
    '''
    firstfive = TopoManip(yeastset, modellist = ["bayes","raxml","BEAST","phyml"], treefilesuff = ["_bayes_treeout.txt","_raxml_treeout.txt","_phyml_treeout.txt"], runNum=1, basedir="c:/seqgen")
    firstfive.setOutPrefix("yeasttest")
    firstfive.setTopoOutPrefix("yeast_topos_run")   
    firstfive.countToposOut()
    firstfive.listTopos()
    firstfive.listEachTopo()
    '''
    for i in range(1,runNum+1):
        for yst in yeastset:
            for m in range(len(models)):
                model_dir = "/" + models[m] + "/"
                treehome = "c:/seqgen/" + yst + str(i) + model_dir
                if not (m == "BEAST"):
                    #findSplits(yst + str(i), treehome, models[m])
                    distTreesAnotherTree(yst + str(i), models[m], rooted=False)
                if (m == "BEAST"):
                    distTreesAnotherTree(yst + str(i), models[m], rooted=True)
                    #findSplits(yst + str(i), treehome, models[m], True)
                
