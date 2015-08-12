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
from distribcompare import distribcompare
from YeastSample import YeastSample

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
    '''
    qq_dir = "c:/seqgen"
    treeleafgrows = ["leaf01sameedges","leaf02sameedges","leaf04sameedges","leaf06sameedges","leaf08sameedges","leaf10sameedges"]
    treeedgegrows = ["edge01CDE","edge02CDE","edge04CDE","edge06CDE","edge08CDE","edge10CDE"] 
    treeleafgrowsgtr = ["leaf01sameedgesgtr","leaf02sameedgesgtr","leaf04sameedgesgtr","leaf06sameedgesgtr","leaf08sameedgesgtr","leaf10sameedgesgtr"]
    treeedgegrowsgtr = ["edge01CDEgtr","edge02CDEgtr","edge04CDEgtr","edge06CDEgtr","edge08CDEgtr","edge10CDEgtr"] 
    treefilesuff = ["_bayes_treeout.txt","_raxml_treeout.txt","_phyml_treeout.txt"]
    models = ["bayes","raxml","phyml"]
    '''
    treenums = [1,2]
    for j in treenums:
        os.chdir(qq_dir)
        outfile = open("treeleafgrowstopotable" + str(j) + ".txt",'w')
        header = "tree,bayesk80,bayesgtr,raxmlk80,raxmlgtr,phymlk80,phymlgtr" + "\n"
        outfile.write(header)
        for i in range(len(treeleafgrows)):
            topocountlist = []
            topocountlistgtr = []
            treek = treeleafgrows[i] + str(j)
            treeg = treeleafgrowsgtr[i] + str(j)
            treeline = treek
           
            for m in range(len(models)):
                treedir = qq_dir + "/" + treek + "/" + models[m] + "/"
                topofile = treek + "_" + models[m] + "_tree_topo.txt"
                treeline = treeline + "," + str(countTopos(topofile,treedir))
                treedir = qq_dir + "/" + treeg + "/" + models[m] + "/"
                topofile = treeg + "_" + models[m] + "_tree_topo.txt"
                treeline = treeline + "," + str(countTopos(topofile,treedir))
            outfile.write(treeline + "\n")
        outfile.close()
    '''
               
            
    '''
    for j in range(len(treeleafgrows)):
        
        treenums = [1,2]
        for i in treenums:
            treek = treeleafgrows[j] + str(i)
            treeg = treeleafgrowsgtr[j] + str(i)
        
            for m in range(len(models)):
                plot_title = "GTRvsK80" + treek + "_" + models[m]
                if not os.path.exists(qq_dir + "/" + plot_title + ".r"):
                    treedir1 = qq_dir + "/" + treek  + "/" + models[m] + "/"  
                    treedir2 = qq_dir + "/" + treeg  + "/" + models[m] + "/" 
                    treefile1 = treedir1 + treek + treefilesuff[m]
                    treefile2 = treedir2 + treeg + treefilesuff[m]
                    gtrvsk80 = distribcompare(plot_title, treefile1, treefile2, qq_dir, t1rooted=False, t2rooted=False, mean_jar = "SturmMean_130704.jar", analysis_jar = "analysis_140702.jar")
                    gtrvsk80.set_dims(xlow=0, xhigh=0.12, ylow=0, yhigh=0.12)
                    gtrvsk80.find_means()
                    gtrvsk80.find_disttomean()
                    gtrvsk80.qq_plot()
                else:
                    print("QQ comparison plot already made for trees " + treeleafgrows[i] + " and model " + models[m])
    
    for j in range(len(treeedgegrows)):

        treenums = [1,2]
        for i in treenums:
            treek = treeedgegrows[j] + str(i)
            treeg = treeedgegrowsgtr[j] + str(i)
                        
            for m in range(len(models)):
                plot_title = "GTRvsK80" + treek + "_" + models[m]
                if not os.path.exists(qq_dir + "/" + plot_title + ".r"):
                    treedir1 = qq_dir + "/" + treek  + "/" + models[m] + "/"  
                    treedir2 = qq_dir + "/" + treeg  + "/" + models[m] + "/" 
                    treefile1 = treedir1 + treek + treefilesuff[m]
                    treefile2 = treedir2 + treeg + treefilesuff[m]
                    gtrvsk80 = distribcompare(plot_title, treefile1, treefile2, qq_dir, t1rooted=False, t2rooted=False, mean_jar = "SturmMean_130704.jar", analysis_jar = "analysis_140702.jar")
                    gtrvsk80.set_dims(xlow=0, xhigh=0.12, ylow=0, yhigh=0.12)
                    gtrvsk80.find_means()
                    gtrvsk80.find_disttomean()
                    gtrvsk80.qq_plot()
                else:
                    print("QQ comparison plot already made for trees " + treeleafgrows[i] + " and model " + models[m])
    '''
    #y1 = YeastSample()
    #y1.loadYeast()
    #y1.createGeneList()
    #y1.makeSampledNexusFile()
    
    #y2 = YeastSample(2)
    #y2.makeSampledNexusFile()
    #y2.concatSampNexus()
    '''
    YDL215C - 26611-29058 = 2447
    YMR186W - 72862-74919 = 2057
    YPL169C - 96292-97071 = 779
    '''
    for i in range(1,21):
        y = YeastSample(i)
        y.makeSampledNexusFile()
   
    yeastset = []
    for i in range(1,21):
        yeaststr = "yeast_" + str(i) + "_genes.nex"
        yeastset.append(yeaststr)
    for yfile in yeastset:
        for i in range(1,3):
            os.chdir(basedir)
            newyfile = yfile.rstrip(".nex") + str(i) + ".nex"
            shutil.copy(yfile,newyfile)
        