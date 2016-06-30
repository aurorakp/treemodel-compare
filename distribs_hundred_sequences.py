from rundistribs import *
from jarutils import *
from MrBayesObj import MrBayesObj
from PhyMLObj import PhyMLObj

if __name__ == '__main__':
    treelist = ["edge01CDE","edge02CDE","edge04CDE","edge06CDE","edge08CDE","edge10CDE"]
    
    #treelist = ["leaf01sameedges","leaf02sameedges","leaf04sameedges","leaf06sameedges","leaf08sameedges","leaf10sameedges"]
    
    for t in treelist: 
         
    
        for i in range (0,100):
            
            tree = t + str(i)            
            treedir = "c:/seqgen/" + tree
            
            runRAxML(tree, treedir)
            makeRAxMLtreeout(tree, treedir)
            copyjars(treedir + "/raxml/")
            findSturmMean(tree, treedir + "/raxml/","raxml")
            tempBayes = MrBayesObj(tree)
            tempBayes.runAll()
            tempPhyML = PhyMLObj(tree)
            tempPhyML.runAll()            
        
#         # Find geodesic distances:    
#         model = "raxml"
#         raxdir = "\\raxml\\"
#         for i in range(0,100):
#             tree = t + str(i)            
#             treedir = "c:/seqgen/" + tree
#             print("Target path is: " + treedir + raxdir)
#             copyGTP(treedir + raxdir)
#             # Base + best + all bootstrap trees
#             geoDistanceMatrix(tree, tree + "_" + model + "_" + "treeout.txt" , treedir + raxdir, model)
