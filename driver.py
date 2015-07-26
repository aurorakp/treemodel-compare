'''
Created on Jul 21, 2015

@author: alkpongsema
'''
from MrBayesObj import MrBayesObj
from RAxMLObj import RAxMLObj
from BEASTObj import BEASTObj
from PhyMLObj import PhyMLObj
from jarutils import *
from LeafNorm import LeafNorm
from LogMapPlotter import LogMapPlotter

def makeSeq(n,tree):
    from SequenceGenerator import SequenceGenerator
    seq_dir = 'c:/seqgen/'
    for i in range(1,n+1):
        shutil.copyfile(seq_dir + tree + ".txt", seq_dir + tree + str(i) + ".txt")
        if not os.path.exists(seq_dir + tree + "\\" + tree + str(i) +  ".nex"):
            tree_gen = SequenceGenerator(tree + str(i),"c:\\seqgen\\" + tree + str(i) +  ".txt")
            tree_gen.runseq_gen()
            shutil.copyfile(seq_dir + tree + str(i) + ".txt", seq_dir + tree + str(i) + "\\" + tree + str(i) + ".txt")
        else:
            print("SeqGen already run for tree " + str(i) + " - skipping sequence generation.")


if __name__ == '__main__':
    
    tree = "seagrass"
    basedir = "c:/seqgen"
    runNum = 2
    
    # 1. Sequence generation
    # makeSeq(10, tree)
    # convert Beauti
    # Create 'treehomes':
    '''
    for i in range(1,11):
        if not os.path.exists(basedir + "/" + tree + str(i) + "/" + tree + str(i) + ".nex"):
            os.chdir(basedir)
            treedir = basedir + "/" + tree + str(i) + "/"
            os.mkdir(treedir)
            copyTree(tree + str(i),basedir + "/",treedir,False)
        else:
            print("Sequences already set up for " + tree + str(i) + " - skipping")
    '''
    # 2. Models
    for i in range(1,runNum):
        '''
        treeBayes = MrBayesObj(tree + str(i))
        treeBayes.prep(False)
        treeBayes.prepScript(nst=2,rates="gamma")
        treeBayes.run()
        treeBayes.runTreeouts()
        
        treeRAxML = RAxMLObj(tree + str(i))
        treeRAxML.prep()
        treeRAxML.run(model="K80-G")
        treeRAxML.runTreeouts()
        '''
        treeBEAST = BEASTObj(tree + str(i))
        treeBEAST.prep()
        treeBEAST.run()
        treeBEAST.runTreeouts()
        
        '''
        treePhyML = PhyMLObj(tree + str(i))
        treePhyML.prep()
        treePhyML.run(model="K80-G")
        treePhyML.runTreeouts()
        '''
    # 3. .jar processing and LeafNorms
        models = ["bayes","raxml","BEAST","phyml"]
        
        # Generate mean tree, distance files, and distance matrices:
        
        for i in range(1,runNum):
            for m in range(len(models)):
                model_dir = "/" + models[m] + "/"
                treehome = basedir + "/" + tree + str(i) + model_dir
                treefiles = [tree + str(i) + "_bayes_treeout.txt",tree + str(i) + "_raxml_treeout.txt",tree + str(i) + "_BEAST_treeout.txt",tree + str(i) + "_phyml_treeout.txt"]
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
            logplot.split_topos()
            logplot.make_centres()
            logplot.make_coords()
            
            #logplot.plot_coords_all()
            #logplot.plot_coords_quads()
            # To delete directories and their contents:
            #shutil.rmtree(treehome + "quadrant_plots")
            #orderByLogMap(tree + str(i), basedir + "/" + tree + str(i), models[m], best=False, orderby=1, bynorm=False)
            #orderByLogMap(tree + str(i), basedir + "/" + tree + str(i), models[m], best=False, orderby=1, bynorm=True)
    
    
   