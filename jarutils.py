'''
Created on Jul 21, 2015

@author: alkpongsema
'''
import os
import re
import shutil
from subprocess import call



def copyjars(treehome):
    gtp_version = "gtp.jar"
    analysis_version = "analysis_140702.jar"
    
    if not os.path.exists(treehome + gtp_version):
        shutil.copyfile('c:\\seqgen\\jars\\' + gtp_version, treehome + gtp_version)
    if not os.path.exists(treehome + analysis_version):
        shutil.copyfile('c:/seqgen/jars/' + analysis_version, treehome + analysis_version)
        
def copyTree(tree,basedir,targetdir,textstart=True):
    if not os.path.exists(targetdir + "\\" + tree):
        if (textstart==True):
            shutil.copyfile(basedir + tree + ".txt",targetdir + tree + ".txt")
        shutil.copyfile(basedir + tree + ".xml", targetdir + tree + ".xml")
        shutil.copyfile(basedir + tree + "_state.xml", targetdir + tree + "_state.xml")
        shutil.copyfile(basedir + tree + ".nex",targetdir + tree + ".nex")
    else:
        print("Tree and NEXUS files already copied for " + tree)

        
def findSturmMean(tree, treehome, model, rooted=False):   
    sturm_version = "SturmMean_130704.jar"
    sturm_file = tree + "_sturm.txt"
    if not os.path.exists(treehome + "\\" + sturm_file):
        shutil.copyfile('c:\\seqgen\\jars\\' + sturm_version, treehome + sturm_version)
        os.chdir(treehome)
        if (rooted == False):
            command = "java -jar " + sturm_version + " -a random -e 0.0001 -u -o " + sturm_file + " " + tree + "_" + model + "_treeout.txt"
        elif (rooted == True):
            command = "java -jar " + sturm_version + " -a random -e 0.0001 -o " + sturm_file + " " + tree + "_" + model + "_treeout.txt"
        call(command.split())
    else:
        print("Mean already found - skipping SturmMean")
        
    # Extract mean tree from file - from my_helper by M. Owen:
    trees_mean = tree + "_mn.txt"
    if not os.path.exists(trees_mean):
        os.chdir(treehome)
        sturmMean_output_file = open(sturm_file,'r')
        outfile = open(trees_mean,'w')
        for line in sturmMean_output_file:
            match_tree = re.match(r'(\(.+)',line)
            if match_tree:
                break
        sturmMean_output_file.close()
        if match_tree:
            outfile.write(match_tree.group(1) + "\n")
            outfile.close()
    else: 
        print ("Warning: could not extract tree from the output file " + sturm_file + "; returning empty string")
        
def geoDistanceMatrix(tree, treefile, treehome, model, distlabel = "", rooted=False):
    os.chdir(treehome)
    gtp_jar = "gtp.jar"
    model_label = "_" + model + "_"
    treelabel = tree + model_label + distlabel
    tree_distances = treelabel + "distances.txt"

    if not os.path.exists(tree_distances):
   
        if (rooted==False):
            command = "java -jar " + gtp_jar + " -u -o " + tree_distances + " " + treefile
            print command
        elif (rooted==True):
            command = "java -jar " + gtp_jar + " -o " + tree_distances + " " + treefile
        call(command.split())
    else:
        print ("Distance file already exists - skipping running Analysis")
        
    tree_dist_matrix = treelabel + "dist_matrix.txt"
    if not os.path.exists(tree_dist_matrix):
        get_diss_matrix(tree_distances,tree_dist_matrix,"symmetric")
    else:
        print ("Distance matrix already exists - skipping running Analysis")
        
def orderByLogMap(tree, treehome, model, best=False, orderby=1, bynorm=False, treeNum=1000):
    # Assumes you've already done the log map to generate 'all coordinates':
    # orderby is the coordinate you would like to organize your trees by
    # the bynorm flag indicates you would like to organize your trees by norm order
    all_coords_file = tree + "_" + model + "_allcoords.txt"
    ordered_coords_file = tree + "_" + model + "_ordered_allcoords.txt"
    ordered_trees_file = tree + "_" + model + "_ordered_treeout.txt"
    treeoutfile = tree + "_" + model + "_treeout.txt"
    
    if (bynorm==True):
        ordered_coords_file = tree + "_" + model + "_norm_ordered_allcoords.txt"
        ordered_trees_file = tree + "_" + model + "_norm_ordered_treeout.txt"
   
    if (best==True):
        all_coords_file = tree + "_" + model + "_best_" + "_allcoords.txt"
        ordered_coords_file = tree + "_" + model + "_best_" + "_ordered_allcoords.txt"
        ordered_trees_file = tree + "_" + model + "_best_" + "_ordered_treeout.txt"
        treeoutfile = tree + "_" + model + "_best_" + "_treeout.txt"
        treeNum = 1001
        
    if (best==True and bynorm==True):
        all_coords_file = tree + "_" + model + "_best_" + "_allcoords.txt"
        ordered_coords_file = tree + "_" + model + "_best_" + "_norm_ordered_allcoords.txt"
        ordered_trees_file = tree + "_" + model + "_best_" + "_norm_ordered_treeout.txt"   
        treeoutfile = tree + "_" + model + "_best_" + "_treeout.txt"
        treeNum = 1001
        
    os.chdir(treehome + "/" + model + "/")
    infile1 = open(all_coords_file,'r')
    coords_y = []
    coords = []
    
    for line in infile1:
        coords.append(line.rstrip("\n"))
        temp = line.split(" ")
        coords_y.append(temp[1])
    infile1.close()
    
    # Sort the coordinates, keeping track of their index:
    if (bynorm == True):
        normfile = open(tree + "_" + model + "_norms.txt",'r')
        norms_n = []
        for line in normfile:
            norms_n.append(line.rstrip("\n"))
            coords_ordered = sorted((e,i) for i,e in enumerate(norms_n))
        normfile.close()    
    else:
        coords_ordered = sorted((e,i) for i,e in enumerate(coords_y))
       
    # Import trees
    trees_raw = []
    infile2 = open(treeoutfile,'r')
    for line in infile2:
        temp = line.rstrip("\n")
        trees_raw.append(temp)
    infile2.close()
    
    # Sort the trees by the coordinates for use in MDS:
    trees_sorted = [None] * treeNum
    #print("Trees_raw length is: " + str(len(trees_raw)) + " for model " + model)
    #print("Coords_ordered length is: " + str(len(coords_ordered)) + " for model " + model)
    for i in range(len(trees_raw)):
        trees_sorted[i] = trees_raw[coords_ordered[i][orderby]]
        
    coords_sorted = [None] * treeNum
    # Sort the coordinates for logmap:
    for i in range(len(coords)):
        coords_sorted[i] = coords[coords_ordered[i][orderby]]
    
    outcoords = open(ordered_coords_file,'w')
    for i in range(len(coords_sorted)):
        if (coords_sorted[i] != None):
            outcoords.write(coords_sorted[i])
    outcoords.close()
    
    outtrees = open(ordered_trees_file,'w')
    for i in range(len(trees_sorted)):
        if (trees_sorted[i] != None):
            outtrees.write(trees_sorted[i] + "\n")
    outtrees.close()
    
    # Created sorted norm output file:
    if (bynorm == True):
        normfile_sorted = open(tree + "_" + model + "_norms_sorted.txt",'w')
        normfile = open(tree + "_" + model + "_norms.txt",'r')
        norms_n = []
        for line in normfile:
            norms_n.append(line.rstrip("\n"))
        normfile.close()
        norms_n.sort()
        for i in range(len(norms_n)):
            normfile_sorted.write(norms_n[i] + "\n")
        normfile_sorted.close()

def convertRootedCoords(tree, treecoordsdir):
    coordsfiles = os.listdir(treecoordsdir)
    for coords_file_name in coordsfiles:
        
        infile = open(coords_file_name,'r')
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
        shutil.copy('tempcoords.txt',treecoordsdir + coords_file_name)
        os.remove('tempcoords.txt')
        
def get_diss_matrix(geo_file_name,diss_file_name,sym_flag):
    '''
    Method from my_helper by M. Owen
    '''
    max_row = 0
    max_col = 0
    # Loop through the geo file the first time to get the dimensions
    # of diss_matrix
    geo_dist_file = open(geo_file_name,'r')
    for line in geo_dist_file:
        match_line = re.match(r'([0-9]+)\s([0-9]+)\s([0-9\.E-]+)',line)
        if (match_line):
            if ( int(match_line.group(1)) > max_row):
                max_row = int(match_line.group(1))
            if ( int(match_line.group(2)) > max_col):
                max_col = int(match_line.group(2))
    geo_dist_file.close()

    # Create and populate the diss_matrix
    geo_dist_file = open(geo_file_name,'r')

    # add one to max_row if symmetric matrix
    # (because last row is not output by GTP because determined by symmetry)
    if (sym_flag == "symmetric"):
        max_row= max_row + 1
        if (max_row != max_col):
            print "Error:  symmetric matrix but read in %d rows and %d columns.  Exiting" % (max_row + 1, max_col +1)
            exit(1)

    # add one because rows/cols were labelled 0, 1, 2, ... by GTP
    diss_matrix = [ [0]*(max_col+1) for x in xrange(max_row+1)]

    # Loop through the geo file the second time to populate diss_matrix
    for line in geo_dist_file:
        match_line = re.match(r'([0-9]+)\s([0-9]+)\s([0-9\.E-]+)',line)

        if (match_line):
            diss_matrix[int(match_line.group(1))][int(match_line.group(2))]    = match_line.group(3)
            if (sym_flag == "symmetric"):
                diss_matrix[int(match_line.group(2))][int(match_line.group(1))]    = match_line.group(3)

    geo_dist_file.close()

    # print the geodesic distances as a dissimilarity matrix to the output file.
    o = open(diss_file_name,'w')

    for row in range(max_row + 1):
        for col in range(max_col + 1):
            o.write(str(diss_matrix[row][col]) + ' ')
        o.write('\n')
    o.close()