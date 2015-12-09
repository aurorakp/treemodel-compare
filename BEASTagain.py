'''
Created on Dec 9, 2015

@author: alkpongsema
'''
from BEASTObj import BEASTObj

from jarutils import *
from LeafNorm import LeafNorm
from LogMapPlotter import LogMapPlotter

if __name__ == '__main__':
    treeleafgrowsgtr = ["leaf01sameedgesgtr","leaf02sameedgesgtr","leaf04sameedgesgtr","leaf06sameedgesgtr","leaf08sameedgesgtr","leaf10sameedgesgtr"]
    treeedgegrowsgtr = ["edge01CDEgtr","edge02CDEgtr","edge04CDEgtr","edge06CDEgtr","edge08CDEgtr","edge10CDEgtr"] 

    for i in range(len(treeleafgrowsgtr)):
        tree = treeleafgrowsgtr[i]
        shutil.copy("c:/BEAST/" + tree + "1.xml","c:/seqgen/" + tree + "1/" + tree + "1.xml")
        shutil.copy("c:/BEAST/" + tree + "1_state.xml","c:/seqgen/" + tree + "1/" + tree + "1_state.xml")
    for i in range(len(treeleafgrowsgtr)):
        tree = treeedgegrowsgtr[i]
        shutil.copy("c:/BEAST/" + tree + "1.xml","c:/seqgen/" + tree + "1/" + tree + "1.xml")
        shutil.copy("c:/BEAST/" + tree + "1_state.xml","c:/seqgen/" + tree + "1/" + tree + "1_state.xml")
    
    runNum = 2;
    
    for i in range(len(treeleafgrowsgtr)):
        tree = treeleafgrowsgtr[i] + "1"
            for i in range(1,runNum):
                '''
                treeBayes = MrBayesObj(tree + str(i))
                treeBayes.prep(False)
                #treeBayes.prepScript(nst=2,rates="gamma")
                treeBayes.prepScript()
                treeBayes.run()
                treeBayes.runTreeouts()
                
                treeRAxML = RAxMLObj(tree + str(i))
                treeRAxML.prep()
                treeRAxML.run()
                treeRAxML.runTreeouts()
                '''
                treeBEAST = BEASTObj(tree + str(i))
                treeBEAST.prep()
                treeBEAST.run()
                treeBEAST.runTreeouts()
                 
                '''
                treePhyML = PhyMLObj(tree + str(i))
                treePhyML.prep()
                treePhyML.run()
                treePhyML.runTreeouts()
                '''
            # 3. .jar processing and LeafNorms
                #models = ["bayes","raxml","BEAST","phyml"]
                #models = ["bayes","raxml","phyml"]
                # Generate mean tree, distance files, and distance matrices:
                models = ["BEAST"]
            
            for i in range(1,runNum+1):
                for m in range(len(models)):
                    model_dir = "/" + models[m] + "/"
                    treehome = basedir + "/" + tree + str(i) + model_dir
                    #treefiles = [tree + str(i) + "_bayes_treeout.txt",tree + str(i) + "_raxml_treeout.txt",tree + str(i) + "_phyml_treeout.txt"]
                    treefiles = [tree + str(i) + "_BEAST_treeout.txt"]
                    copyjars(treehome)
                    if (models[m] == "BEAST"):
                        findSturmMean(tree + str(i), treehome, models[m], rooted=True)
                        geoDistanceMatrix(tree + str(i), treefiles[m], treehome, models[m], distlabel = "", rooted=True)
                    else:
                        findSturmMean(tree + str(i), treehome, models[m], rooted=False)
                        geoDistanceMatrix(tree + str(i), treefiles[m], treehome, models[m], distlabel = "", rooted=False)
                    '''
                    if not os.path.exists(treehome + tree + str(i) + "_" + models[m] + "_norms.txt"):
                        ln = LeafNorm(tree + str(i), treefiles[m], treehome, models[m])
                        ln.makeNormFiles()
                    '''
                        
            # 4. Coordinate discovery for logmaps
            #models = ["bayes","raxml","phyml"]
            #models = ["bayes"]
            models = ["BEAST"]
            for i in range(1,runNum+1):
                for m in range(len(models)):
                    model_dir = "/" + models[m] + "/"
                    treehome = basedir + "/" + tree + str(i) + model_dir
                    #treefiles = [tree + str(i) + "_bayes_treeout.txt",tree + str(i) + "_raxml_treeout.txt",tree + str(i) + "_phyml_treeout.txt"]
                    treefiles = [tree + str(i) + "_BEAST_treeout.txt"]
                    #treefiles = [tree + str(i) + "_raxml_treeout.txt",tree + str(i) + "_BEAST_treeout.txt",tree + str(i) + "_phyml_treeout.txt"]
                    logplot = LogMapPlotter(tree + str(i), treefiles[m], treehome, models[m], rooted=True)
                    #logplot = LogMapPlotter(tree + str(i), treefiles[m], treehome, models[m], rooted=False)
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
       
