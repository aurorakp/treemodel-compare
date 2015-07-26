import os
import topology_file_splitter
import subprocess
import re

# code version
analysis_version = "analysis_140702.jar"

# output files
tree_name = "baserescaled"
trees_file_name = tree_name + "treeout.txt"
#trees_file_name = tree_name + "_raxmlout.txt"
trees_topo_name = tree_name + "_tree_topo.txt"
all_topos_coords_centre1 = tree_name + "_allcoords.txt"



# output dirs and prefixes
topo_dir = "split_by_topology"
coords_dir = "coords"
centre_dir = "centres"
plots_dir = "quadrant_plots"

topo_prefix = topo_dir + "/topo.txt"
coords_prefix = coords_dir + "/coords_"
centre_prefix = centre_dir + "/centre_"
plots_all = plots_dir + "/allplots.txt"



# Run Daniel's code to split up the tree file by topology.
if not os.path.exists(topo_dir):
   os.mkdir(topo_dir)

   topology_file_splitter.makeFiles(trees_file_name,trees_topo_name,topo_prefix)
else:
	print "Directory %s already exists - skipping splitting the means by topology \n" % topo_dir

# Make a set of files with the tree with each topology and 0 branch lengths to use as log map center.


if not os.path.exists(centre_dir):
    os.mkdir(centre_dir)
    f = open(trees_topo_name)
    topNum = 0
    # Extract the number of topologies from the topology file
    for line in f:
        tempStr = line
        if (tempStr[0:3] != "Raw"):
            continue
        else: 
            trimStr = tempStr.lstrip("Raw topology counts:  ").split()
            topNum = len(trimStr)
            break
    f.close()
    
    
    for n in xrange(1,topNum+1):
        
        testout = centre_prefix + str(n)
        tree_file_name = topo_dir + '/topo' + str(n) + '.txt'
        f = open(tree_file_name,'r')
        tree = f.readline()
        
        #if (n == 4):
        #    m = re.match(r'(\(+[A-Z]:[0-9]+[.][0-9]+,[A-Z]:[0-9]+[.][0-9]+\):)[0-9]+[.][0-9]+(,\([A-Z]:[0-9]+[.][0-9]+,[A-Z]:[0-9]+[.][0-9]\):)[0-9]+[.][0-9]+(,.+)',tree)
        #elif (n == 5):
        #    m = re.match(r'(\(+[A-Z]:[0-9]+[.][0-9]+,[A-Z]:[0-9]+[.][0-9]+\):)[0-9]+[.][0-9]+(,[A-Z]:[0-9]+[.][0-9]+\):)[0-9]+.[0-9]+(,.+)',tree)
        #else:
        m = re.match(r'(.*?\):)[0-9]+[.][0-9]+(.*?\):)[0-9]+[.][0-9]+(.+;)',tree)
        
            
        #if (n == 1):
        #    m = re.match(r'(\(\(\(.+\):).+(,.+\):).+(,[A-Z]:[0-9][.][0-9]+[a-z][-][0-9]+,[A-Z]:[0-9][.][0-9]+[a-z][+][0-9]+\);)',tree)
        #if (n == 2):
        #    m = re.match(r'(\(\(\(.+\):).+(,.+\):).+(,[A-Z]:[0-9][.][0-9]+[a-z][-][0-9]+,[A-Z]:[0-9][.][0-9]+[a-z][+][0-9]+\);)',tree)
        #print 'n is: ' + str(n)
        #if (n == 4):
        #    m = re.match(r'(\(\(.+\):).+(,\(.+\):).+(,.+\);)',tree)
        #elif (n == 3):
        #    m = re.match(r'(\(\(\(.+\):).+(,.+\):).+(,[A-Z]:[0-9][.][0-9]+[a-z][+][0-9]+,[A-Z]:[0-9][.][0-9]+[a-z][+][0-9]+\);)',tree)
        #else:
        #    m = re.match(r'(\(\(\(.+\):).+(,.+\):).+(,[A-Z]:[0-9][.][0-9]+[a-z][-][0-9]+,[A-Z]:[0-9][.][0-9]+[a-z][+][0-9]+\);)',tree)
        
        if not m:
            print("Error:  can't change interior edges lengths")
            exit
        tree = m.group(1) + '0.000000001' + m.group(2) + '0.000000001' + m.group(3)
        out = open(centre_prefix + str(n),'w')
        out.write(tree + '\n')
        out.close()
        f.close()


# Compute the log map coords for each topology file.  Just use the first tree in the file
# as centre tree.

if not os.path.exists(coords_dir):
   os.mkdir(coords_dir)
   for topo_file_name in os.listdir(topo_dir):
      # get the number at the end of the file name
      match_file_name = re.match(r'topo([0-9]+).txt',topo_file_name)
      i = int(match_file_name.group(1))
      command = 'java -jar ' + analysis_version + ' -u -a log_map -o ' + coords_prefix + str(i) + '.txt -f ' + centre_prefix + str(i) + ' ' + topo_dir +'/' +topo_file_name
      subprocess.call(command.split())
else:
   	print "Directory %s already exists - skipping computing the log map coordinates \n" % coords_dir

if not os.path.exists(all_topos_coords_centre1):
    
    command = 'java -jar ' + analysis_version + ' -u -a log_map -o ' + all_topos_coords_centre1 + ' -f ' + centre_prefix + "1" + ' ' + trees_file_name
    subprocess.call(command.split())
    
   
if not os.path.exists(plots_dir):
    os.mkdir(plots_dir)
    os.chdir('c:\\pystuff\\bioscripting\\test\\')
    command = 'C:\\Rstuff\\R-3.2.0\\bin\\Rscript.exe ' + 'c:\\pystuff\\bioscripting\\test\\plot_coords.r'
    subprocess.call(command.split())
    #command = 'rscript plot_coords.r'
    #call(command.split())
else:
    print "Quadrants already plotted - skipping quadrant creation"
    
if not os.path.exists(plots_all):
    command = 'C:\\Rstuff\\R-3.2.0\\bin\\Rscript.exe ' + 'c:\\pystuff\\bioscripting\\test\\plot_allcoords.r'
    subprocess.call(command.split())
else:
    print "All topologies already plotted - skipping plot creation"


   
 
