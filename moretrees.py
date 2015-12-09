'''
Created on Oct 12, 2015

@author: alkpongsema
'''

import os
from subprocess import call
import topology_file_splitter
from test.BayesExtract import BayesExtract


if __name__ == '__main__':
    
    basedir = "c:/christianfiles/"
    tree_name = "newbase"
    treehome = basedir + tree_name
    trees_file_name = treehome + "/" + tree_name + "treeout.txt"
    topo_dir = treehome + "/split_by_topology_2000"
    topo_dir + "/topo.txt"
    topo_prefix = topo_dir + "/topo.txt"
    analysis_version = "analysis_140702.jar"
    
    os.chdir(treehome)
    b1 = BayesExtract(tree_name, "newbase.nex",outpath=treehome,treeNum=2000)
    b1.treeMatch()
    
    trees_topo_file_name =  tree_name + "_bayes"+ "_tree_2000_topo.txt"

    # Get topology information about the tree file.
    if not os.path.exists(trees_topo_file_name):
        os.chdir(treehome)
        command = "java -jar " + analysis_version + " -a topology_count -o " + trees_topo_file_name + " " + trees_file_name
        call(command.split())
    else:
        print "File %s already exists - skipping generating topology info about trees \n" % trees_topo_file_name


    if not os.path.exists(topo_dir):
        os.mkdir(topo_dir)
                   
        topology_file_splitter.makeFiles(trees_file_name,trees_topo_file_name,topo_prefix)
    else:
        print "Directory %s already exists - skipping splitting the trees by topology \n" % topo_dir
