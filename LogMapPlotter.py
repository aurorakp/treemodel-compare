'''
Created on Jul 9, 2015

@author: alkpongsema
'''

import os
import topology_file_splitter
import subprocess
import re
import shutil
from make_rplotscript import make_rplotscript
from LeafNorm import LeafNorm

class LogMapPlotter(object):
    '''
    Takes in a tree file, directory to use, and splits by topology, finds centers, coordinates, and plots tree topologies using
    the log map geodesic distance.  Note: treehome should be the model directory i.e. c:/seqgen/onetenth1/bayes/ 
    '''


    def __init__(self, treename, treefile, treehome, model, rooted=False):
        self.analysis_version = "analysis_140702.jar"
        self.tree_name = treename
        self.model = model
        self.trees_file_name = treefile
        self.trees_topo_name = self.tree_name + "_" + model + "_" + "tree_topo.txt"
        self.ordered = self.setOrdered()
        self.all_topos_coords_centre = self.tree_name + "_" + model + self.ordered + "_allcoords.txt"
        self.treehome = treehome
        self.topNum = 0
        self.rooted = rooted
        self.Rpath = "C:\\Rstuff\\R-3.2.0\\bin\\Rscript.exe"
               
        # output dirs and prefixes
        self.topo_dir = treehome + "split_by_topology"
        self.coords_dir = treehome + "coords"
        self.centre_dir = treehome + "centres"
        self.plots_dir = treehome + "quadrant_plots"
        
        self.topo_prefix = self.topo_dir + "/topo.txt"
        self.coords_prefix = self.coords_dir + "/coords_"
        self.centre_prefix = self.centre_dir + "/centre_"
        self.coords_filepref = "coords_"
        self.centre_all_prefix = treehome + treename + "_" + model + "_centre_"
        self.plots_all = self.tree_name + model + "_allcoords.r"
    
    def setTopNum(self):
        f = open(self.trees_topo_name)
        topNum = 0
        # Extract the number of topologies from the topology file
        for line in f:
            tempStr = line
            if (tempStr[0:3] != "Raw"):
                continue
            else: 
                trimStr = tempStr.lstrip("Raw topology counts:  ").split()
                topNum = len(trimStr)
                self.topNum = topNum
                break
        print("TopNum is: " + str(self.topNum))
        f.close()
    
    def setOrdered(self,ordered=False):   
        if (ordered == False):
            return ""
        elif (ordered == True):
            return "_ordered"
            
    def split_topos(self):
        # Run Daniel's code to split up the tree file by topology.
        analysis_version = "analysis_140702.jar"
        
        trees_topo_file_name =  self.tree_name + "_" + self.model + "_tree_topo.txt"

        # Get topology information about the tree file.
        if not os.path.exists(trees_topo_file_name):
            os.chdir(self.treehome)
            command = "java -jar " + analysis_version + " -a topology_count -o " + trees_topo_file_name + " " + self.trees_file_name
            subprocess.call(command.split())
        else:
            print "File %s already exists - skipping generating topology info about trees \n" % trees_topo_file_name
    
    
        if not os.path.exists(self.topo_dir):
            os.mkdir(self.topo_dir)
                       
            topology_file_splitter.makeFiles(self.trees_file_name,self.trees_topo_name,self.topo_prefix)
        else:
            print "Directory %s already exists - skipping splitting the trees by topology \n" % self.topo_dir

    # Make a set of files with the tree with each topology and 0 branch lengths to use as log map center.
    def make_centres(self,desiredTopo=1):
        
        
        if not os.path.exists(self.centre_dir):
            os.mkdir(self.centre_dir)
            f = open(self.trees_topo_name)
            topNum = 0
            # Extract the number of topologies from the topology file
            for line in f:
                tempStr = line
                if (tempStr[0:3] != "Raw"):
                    continue
                else: 
                    trimStr = tempStr.lstrip("Raw topology counts:  ").split()
                    topNum = len(trimStr)
                    self.topNum = topNum
                    break
            print("TopNum is: " + str(self.topNum))
            f.close()
            
            for n in range(1,topNum+1):

                tree_file_name = self.topo_dir + '/topo' + str(n) + '.txt'
                f = open(tree_file_name,'r')
                tree = f.readline()
                if (self.rooted == False):
                    m = re.match(r'(.*?\):)[0-9]+[.][0-9]+(.*?\):)[0-9]+[.][0-9]+(.+;)',tree)
                    if not m:
                        print("Error:  can't change interior edges lengths")
                        exit
                    tree = m.group(1) + '0.000000001' + m.group(2) + '0.000000001' + m.group(3)
                
                elif (self.rooted == True):
                    m = re.match(r'(.*?\):)[0-9]+[.][0-9]+(.*?\):)[0-9]+[.][0-9]+(.*?\):)[0-9]+[.][0-9]+(.*?;)',tree)
                    if not m:
                        print("Tree that caused error: " + tree)
                        print("Error:  can't change interior edges lengths")
                        exit
                    tree = m.group(1) + '0.000000001' + m.group(2) + '0.000000001' + m.group(3) + '0.000000001' + m.group(4)
                    if (tree[-1] != ";"):
                        tree = tree + ";"
        
                out = open(self.centre_prefix + str(n),'w')
                out.write(tree + '\n')
                out.close()
                f.close()
    # First, for the 'overall' center, make sure to use the first tree for the topology we want
        tree_file_name = self.topo_dir + '/topo' + str(desiredTopo) + '.txt'
        os.chdir(self.topo_dir)
        f = open(tree_file_name)
        tree = f.readline()
        # Note: below methods work with trees in scientific notation as adding an 'e-003' at the end only makes
        # the centre smaller and closer to the origin - has no significant effect on the tree
        if not (self.rooted==True):
            m = re.match(r'(.*?\):)[0-9]+[.][0-9]+(.*?\):)[0-9]+[.][0-9]+(.+;)',tree)
            if not m:
                    print("Error:  can't change interior edges lengths")
                    exit
            tree = m.group(1) + '0.000000001' + m.group(2) + '0.000000001' + m.group(3)
        if (self.rooted==True):
            m = re.match(r'(.*?\):)[0-9]+[.][0-9]+(.*?\):)[0-9]+[.][0-9]+(.*?\):)[0-9]+[.][0-9]+(.*?;)',tree)
            if not m:
                print("Error:  can't change interior edges lengths")
                exit
            tree = m.group(1) + '0.000000001' + m.group(2) + '0.000000001' + m.group(3) + '0.000000001' + m.group(4)
            if (tree[-1] != ";"):
                tree = tree + ";"
        out = open(self.centre_all_prefix,'w')
        out.write(tree + '\n')
        out.close()
        f.close()
        
    
        
    # Compute the log map coords for each topology file.  Just use the first tree in the file
    # as centre tree.
    
    def make_coords(self, desiredTopo=1):
        #'''        
        #if not os.path.exists(self.coords_dir):
        #    os.mkdir(self.coords_dir)
        #    os.chdir(self.treehome)
        #    for topo_file_name in os.listdir(self.topo_dir):
        #        # get the number at the end of the file name
        #        match_file_name = re.match(r'topo([0-9]+).txt',topo_file_name)
        #        i = int(match_file_name.group(1))
        #        if (self.rooted == False):
        #            command = 'java -jar ' + self.analysis_version + ' -u -a log_map -o ' + self.coords_prefix + str(i) + '.txt -f ' + self.centre_prefix + str(i) + ' ' + self.topo_dir +'/' + topo_file_name
        #        else:
        #            command = 'java -jar ' + self.analysis_version + ' -a log_map -o ' + self.coords_prefix + str(i) + '.txt -f ' + self.centre_prefix + str(i) + ' ' + self.topo_dir +'/' + topo_file_name   
        #        subprocess.call(command.split())
        #        
        #        coords_file_name = "coords_" + str(i) + ".txt"
        #        
        #        if (self.rooted == True):
        #            self.convertRootedCoords(coords_file_name, self.coords_dir)
        #        
        #        #cl = LeafNorm(self.tree_name, self.topo_dir + "/" + topo_file_name, self.treehome, self.model)
        #        #cl.setNormOut(self.coords_dir + "/" + coords_file_name[:-4] + "_norms.txt")
        #        #cl.makeNormFiles()
        #    
        #else:
        #        print "Directory %s already exists - skipping computing the log map coordinates \n" % self.coords_dir
        
        os.chdir(self.treehome)
        if not os.path.exists(self.all_topos_coords_centre):
            if (self.rooted == False):
                command = 'java -jar ' + self.analysis_version + ' -u -a log_map -o ' + self.all_topos_coords_centre + ' -f ' + self.centre_prefix + "1" + ' ' + self.trees_file_name
                subprocess.call(command.split())
            else:
                command = 'java -jar ' + self.analysis_version + ' -a log_map -o ' + self.all_topos_coords_centre + ' -f ' + self.centre_prefix + "1" + ' ' + self.trees_file_name
                subprocess.call(command.split())
                coords_file_name = self.all_topos_coords_centre
                self.convertRootedCoords(coords_file_name, self.treehome.rstrip("//"))
                
    
    def convertRootedCoords(self, treecoordfile, treecoordsdir):
        os.chdir(treecoordsdir)
        if not os.path.exists("origcoords"):
            os.mkdir("origcoords")
        # Make a copy of the original coordinates for future MDS use
        shutil.copy(treecoordfile, treecoordsdir + "/origcoords/" + treecoordfile)
        infile = open(treecoordfile,'r')
        outfile = open('tempcoords.txt','w')
        for line in infile:
            coordholder = line.rstrip("\n").split(" ")
            # Add the second and third coordinates together to 'fix' the split lengths
            # due to BEAST (or another model) auto-rooting the output trees
            coordsum = float(coordholder[1]) + float(coordholder[2])
            coordholder[1] = str(coordsum)
            coordtemp = ""
            for i in range(len(coordholder)):
                coordtemp = coordtemp + coordholder[i] + " "
            outfile.write(coordtemp + "\n")
        infile.close()
        outfile.close()
        os.remove(treecoordfile)
        shutil.copy('tempcoords.txt',treecoordsdir + "/" +  treecoordfile)
        os.remove('tempcoords.txt')
        
    def plot_coords_quads(self):
        
        print("plots dir is: " + self.plots_dir)
        if not os.path.exists(self.plots_dir):
            os.mkdir(self.plots_dir)
            #os.chdir(self.treehome)
            self.setTopNum()
            print "TopNum is: " + str(self.topNum)
            for i in range(1,self.topNum+1):
                os.chdir(self.plots_dir)
                logplot = make_rplotscript(self.coords_dir, self.coords_filepref + str(i) + '.txt', self.tree_name + " Topology " + str(i) + " Logmap", aspect_ratio=1, outdir = self.plots_dir, mean=False, majority=False)
                logplot.rplot()
                #logplot.setNormFile(self.coords_prefix + str(i) + "_norms.txt")
                #logplot.rplotnorm()
                command = self.Rpath + ' ' + self.coords_dir + "/" + self.coords_filepref + str(i) + '.r'
                #command = 'C:\\Rstuff\\R-3.2.0\\bin\\Rscript.exe ' + self.coords_dir + "/" + self.coords_filepref + str(i) + '.r'
                subprocess.call(command.split())
                #normcommand =  'C:\\Rstuff\\R-3.2.0\\bin\\Rscript.exe ' + self.coords_dir +"/" + self.coords_filepref + str(i) + "_norm3D.r"
                #subprocess.call(normcommand.split())
        else:
            print "Quadrants already plotted - skipping quadrant creation"
    
    def plot_coords_all(self):
        os.chdir(self.treehome)
        if not os.path.exists(self.plots_all):
            allplot = make_rplotscript(self.treehome, self.all_topos_coords_centre, self.tree_name + " All Topologies Relative to Centre 1 Logmap", aspect_ratio=1, outdir = self.treehome, mean=False, majority=False)
            allplot.rplot()
            #allplot.setNormFile(self.treehome + self.tree_name + "_" + self.model + "_norms.txt")
            #allplot.rplotnorm()
            #command = 'C:\\Rstuff\\R-3.2.0\\bin\\Rscript.exe ' + self.treehome + self.all_topos_coords_centre[0:-4] +  self.ordered + '.r'
            command = self.Rpath + ' ' + self.treehome + "/" + self.all_topos_coords_centre[0:-4] +  self.ordered + '.r'
            print("command is: " + command)
            subprocess.call(command.split())
            #normcommand = 'C:\\Rstuff\\R-3.2.0\\bin\\Rscript.exe ' + self.treehome + self.all_topos_coords_centre[0:-4] +  self.ordered + '_norm3D.r'
            #subprocess.call(normcommand.split())
        else:
            print "All topologies already plotted - skipping plot creation"
            
            
    def logplot(self):
        self.split_topos()
        self.make_centres()
        self.make_coords()
        self.plot_coords()