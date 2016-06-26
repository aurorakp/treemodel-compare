from rundistribs import *
from jarutils import *
from MrBayesObj import MrBayesObj
from PhyMLObj import PhyMLObj
from RAxMLObj import RAxMLObj
from YeastSample import YeastSample
import os

if __name__ == '__main__':
    
    yeastlist = []
    
    
    # Set seeds for random and sample the Yeast genes:
    for j in range(1,101):
        for i in range(1,21):
            #y = YeastSample(i,j)
            #y.makeSampledNexusFile()
            
            # Add each yeast tree (gene and seed number) to the list of yeasts: 
            yeastlist.append("yeast_" + str(i) + "_genes_" + str(j) + "_seed")
            
    for yeast in yeastlist: 
         
    
              
        tree = yeast          
        treedir = "c:/seqgen/" + yeast
        if not os.path.exists(treedir):
            os.chdir("c:/seqgen")
            os.mkdir(treedir)
            shutil.copy("c:/seqgen/" + yeast + ".nex", treedir + "/" + yeast + ".nex")
            
          
        runRAxML(tree, treedir)
        #makeRAxMLtreeout(tree, treedir)
        tempBayes = MrBayesObj(tree)
        tempBayes.runAllYeast()
        tempPhyML = PhyMLObj(tree)
        tempPhyML.runAll()            