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

if __name__ == '__main__':
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