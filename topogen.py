'''
Created on Nov 16, 2015

@author: alkpongsema
'''
import os
import re

if __name__ == '__main__':
    
    
    basedir = "c:/seqgen/"
    os.chdir(basedir)
    models = ["bayes","raxml","phyml"]
    topodir = "split_by_topology/"
    topoprefix = "/topo.txt"
    # Compare topologies
    # Steps:
    
    # Extract topologies from each run
    # 1. By Model
    # 2. By Run (all runs)
    # format:  topology  number of trees
    
    # Creating a spot to put all this:
    edgeleaftopodir = basedir + "edgesandleaves"
    edgeleafstr = ["01","02","04","06","08","10"]
    
    
    # Extract by model and run:
    
    # first, for the leaves:
    
    for estr in edgeleafstr:
        for m in range(len(models)):
            modeldir = models[m] + "/"
            topoloc = basedir + "leaf" + estr + "sameedgesgtr1/" + modeldir
            topofile = topoloc + "leaf" + estr + "sameedgesgtr1_" + models[m] + "_tree_topo.txt"
            infile = open(topofile,'r')
            outfile = open(edgeleaftopodir + "/leaf" + estr + "_" + models[m] + "_toposummary.txt",'w')
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
    
    # Then, for the edges:
    
    for estr in edgeleafstr:
        for m in range(len(models)):
            modeldir = models[m] + "/"
            topoloc = basedir + "edge" + estr + "CDEgtr1/" + modeldir
            topofile = topoloc + "edge" + estr + "CDEgtr1_" + models[m] + "_tree_topo.txt"
            infile = open(topofile,'r')
            outfile = open(edgeleaftopodir + "/edge_" + estr + "_" + models[m] + "_toposummary.txt",'w')
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