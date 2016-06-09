'''
Created on Sep 24, 2015

@author: alkpongsema
'''
import os
import shutil
from subprocess import call
import topology_file_splitter
import re

if __name__ == '__main__':
    
    geneNum = 20
    basedir = "c:/seqgen/"
    os.chdir(basedir)
    models = ["bayes","BEAST","raxml","phyml"]
    
    # Concatenate for each model:
    '''
    for m in range(len(models)):
        modeldir = models[m] + "/"
        allmodel = "yeast_all_" + models[m] + "_treeouts.txt"
        outfile = open(allmodel,'w')    
        for i in range(1,geneNum + 1):
            yeast_string = "yeast_" + str(i) + "_genes1" 
            file_string = yeast_string + "_" + models[m] + "_treeout.txt"
            yeast_fileloc = basedir + yeast_string + "/" + modeldir + file_string
            infile = open(yeast_fileloc, 'r')
            for line in infile:
                outfile.write(line)
            infile.close()
        outfile.close()
    
    # Concatenate all models:
    
    outfile_all = "yeast_allgenes_allmodels_treeout.txt"
    for m in range(len(models)):
        modeldir = models[m] + "/"
        outfile = open(outfile_all,'w')    
        for i in range(1,geneNum + 1):
            yeast_string = "yeast_" + str(i) + "_genes1" 
            file_string = yeast_string + "_" + models[m] + "_treeout.txt"
            yeast_fileloc = basedir + yeast_string + "/" + modeldir + file_string
            infile = open(yeast_fileloc, 'r')
            for line in infile:
                outfile.write(line)
            infile.close()
    outfile.close()
    '''
    analysis_version = "analysis_140702.jar"
    
    '''
    for m in range(len(models)):
        trees_topo_file_name = "yeast_" + "all" + "_" + models[m] + "_tree_topo.txt"
        trees_treeout = "yeast_" + "all" + "_" + models[m] + "_treeouts.txt"
        topo_dir = "yeastall" + "_" + models[m]
        topo_prefix = basedir + topo_dir + "/topo.txt"
        # Get topology information about the tree file.
        if not os.path.exists(trees_topo_file_name):
            command = "java -jar " + analysis_version + " -a topology_count -o " + trees_topo_file_name + " " + trees_treeout
            call(command.split())
        else:
            print "File %s already exists - skipping generating topology info about trees \n" % trees_topo_file_name
    
    
        if not os.path.exists(topo_dir):
            os.mkdir(topo_dir)
                       
            topology_file_splitter.makeFiles(trees_treeout,trees_topo_file_name,topo_prefix)
        else:
            print "Directory %s already exists - skipping splitting the trees by topology \n" % topo_dir
    
    trees_topo_file_name = "yeast_" + "all" + "_allmodels" + "_tree_topo.txt"
    trees_treeout = "yeast_" + "allgenes" + "_allmodels" + "_treeout.txt"
    topo_dir = "yeastall" + "_allmodels"  
    topo_prefix = basedir + topo_dir + "/topo.txt"
    # Get topology information about the tree file.
    if not os.path.exists(trees_topo_file_name):
        command = "java -jar " + analysis_version + " -a topology_count -o " + trees_topo_file_name + " " + trees_treeout
        call(command.split())
    else:
        print "File %s already exists - skipping generating topology info about trees \n" % trees_topo_file_name


    if not os.path.exists(topo_dir):
        os.mkdir(topo_dir)
                   
        topology_file_splitter.makeFiles(trees_treeout,trees_topo_file_name,topo_prefix)
    else:
        print "Directory %s already exists - skipping splitting the trees by topology \n" % topo_dir
    '''
        
    
    # Compare topologies
    # Steps:
    topodir = "split_by_topology/"
    topoprefix = "/topo.txt"
    # Extract topologies from each run
    # 1. By Model
    # 2. By Run (all runs)
    # format:  topology  number of trees
    
    # Creating a spot to put all this:
    os.mkdir("yeasttopodata")
    yeasttopodir = basedir + "yeasttopodata"
    
    # Extract by model and run:
    for i in range(1,geneNum + 1):
        for m in range(len(models)):
            modeldir = models[m] + "/"
            topoloc = basedir + "yeast_" + str(i) + "_genes1/" + modeldir
            topofile = topoloc + "yeast_" + str(i) + "_genes1_" + models[m] + "_tree_topo.txt"
            infile = open(topofile,'r')
            outfile = open(yeasttopodir + "/yeast_" + str(i) + "_" + models[m] + "_toposummary.txt",'w')
            outfile.write("topology treeNumber" + "\n")
            stop = False
            topo = False
            linewrite = ""
            for line in infile:
                
                temp = line.split()
                
                # If you hit the 'Raw topology counts' line, you are done:
                
                if (temp[0] == "Raw"):
                    stop = True
                elif (stop == True):
                    break
             
                else:
                    
                    # If you found a topology listed on the previous line, get the number of
                    # trees in that topology and write the line 
                    
                    if (topo == True):
                        linewrite = linewrite + " " + temp[0] + "\n"
                        outfile.write(linewrite)
                        topo = False
                        linewrite = ""
                    
                    # Look for the topology list and save it to the line to write:
                        
                    else:
                        m = re.match(r'([0-9]).',temp[0])
                        if m:
                            linewrite = linewrite +  temp[1]
                            topo = True
                            
            
            outfile.close()        
                        
                        
                            
        
    
    # Compare them (using R) with Ape
    
    # Condense them (using R)
    # output format:  topology (merged) number of trees
    # Collect data
    
    
    geneNum = 20
    basedir = "c:/seqgen/"
    os.chdir(basedir)
    models = ["bayes","BEAST","raxml","phyml"]
    
    # Concatenate for each model:
    '''
    for m in range(len(models)):
        modeldir = models[m] + "/"
        allmodel = "yeast_all_" + models[m] + "_treeouts.txt"
        outfile = open(allmodel,'w')    
        for i in range(1,geneNum + 1):
            yeast_string = "yeast_" + str(i) + "_genes1" 
            file_string = yeast_string + "_" + models[m] + "_treeout.txt"
            yeast_fileloc = basedir + yeast_string + "/" + modeldir + file_string
            infile = open(yeast_fileloc, 'r')
            for line in infile:
                outfile.write(line)
            infile.close()
        outfile.close()
    
    # Concatenate all models:
    
    outfile_all = "yeast_allgenes_allmodels_treeout.txt"
    for m in range(len(models)):
        modeldir = models[m] + "/"
        outfile = open(outfile_all,'w')    
        for i in range(1,geneNum + 1):
            yeast_string = "yeast_" + str(i) + "_genes1" 
            file_string = yeast_string + "_" + models[m] + "_treeout.txt"
            yeast_fileloc = basedir + yeast_string + "/" + modeldir + file_string
            infile = open(yeast_fileloc, 'r')
            for line in infile:
                outfile.write(line)
            infile.close()
    outfile.close()
    '''
    analysis_version = "analysis_140702.jar"
    
    '''
    for m in range(len(models)):
        trees_topo_file_name = "yeast_" + "all" + "_" + models[m] + "_tree_topo.txt"
        trees_treeout = "yeast_" + "all" + "_" + models[m] + "_treeouts.txt"
        topo_dir = "yeastall" + "_" + models[m]
        topo_prefix = basedir + topo_dir + "/topo.txt"
        # Get topology information about the tree file.
        if not os.path.exists(trees_topo_file_name):
            command = "java -jar " + analysis_version + " -a topology_count -o " + trees_topo_file_name + " " + trees_treeout
            call(command.split())
        else:
            print "File %s already exists - skipping generating topology info about trees \n" % trees_topo_file_name
    
    
        if not os.path.exists(topo_dir):
            os.mkdir(topo_dir)
                       
            topology_file_splitter.makeFiles(trees_treeout,trees_topo_file_name,topo_prefix)
        else:
            print "Directory %s already exists - skipping splitting the trees by topology \n" % topo_dir
    
    trees_topo_file_name = "yeast_" + "all" + "_allmodels" + "_tree_topo.txt"
    trees_treeout = "yeast_" + "allgenes" + "_allmodels" + "_treeout.txt"
    topo_dir = "yeastall" + "_allmodels"  
    topo_prefix = basedir + topo_dir + "/topo.txt"
    # Get topology information about the tree file.
    if not os.path.exists(trees_topo_file_name):
        command = "java -jar " + analysis_version + " -a topology_count -o " + trees_topo_file_name + " " + trees_treeout
        call(command.split())
    else:
        print "File %s already exists - skipping generating topology info about trees \n" % trees_topo_file_name


    if not os.path.exists(topo_dir):
        os.mkdir(topo_dir)
                   
        topology_file_splitter.makeFiles(trees_treeout,trees_topo_file_name,topo_prefix)
    else:
        print "Directory %s already exists - skipping splitting the trees by topology \n" % topo_dir
    '''
        
    
    # Compare topologies
    # Steps:
    topodir = "split_by_topology/"
    topoprefix = "/topo.txt"
    # Extract topologies from each run
    # 1. By Model
    # 2. By Run (all runs)
    # format:  topology  number of trees
    
    # Creating a spot to put all this:
    os.mkdir("yeasttopodata")
    yeasttopodir = basedir + "yeasttopodata"
    
    # Extract by model and run:
    for i in range(1,geneNum + 1):
        for m in range(len(models)):
            modeldir = models[m] + "/"
            topoloc = basedir + "yeast_" + str(i) + "_genes1/" + modeldir
            topofile = topoloc + "yeast_" + str(i) + "_genes1_" + models[m] + "_tree_topo.txt"
            infile = open(topofile,'r')
            outfile = open(yeasttopodir + "/yeast_" + str(i) + "_" + models[m] + "_toposummary.txt",'w')
            outfile.write("topology treeNumber" + "\n")
            stop = False
            topo = False
            linewrite = ""
            for line in infile:
                
                temp = line.split()
                
                # If you hit the 'Raw topology counts' line, you are done:
                
                if (temp[0] == "Raw"):
                    stop = True
                elif (stop == True):
                    break
             
                else:
                    
                    # If you found a topology listed on the previous line, get the number of
                    # trees in that topology and write the line 
                    
                    if (topo == True):
                        linewrite = linewrite + " " + temp[0] + "\n"
                        outfile.write(linewrite)
                        topo = False
                        linewrite = ""
                    
                    # Look for the topology list and save it to the line to write:
                        
                    else:
                        m = re.match(r'([0-9]).',temp[0])
                        if m:
                            linewrite = linewrite +  temp[1]
                            topo = True
                            
            
            outfile.close()        

    
    
    
    