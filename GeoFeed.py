'''
Created on Jun 5, 2015

@author: alkpongsema
'''

from my_helper import *
from operator import itemgetter, attrgetter
import os
import subprocess
import networkx as nx


class GeoFeed(object):
    '''
    Calls GTP to calculate the distances between trees, creates the distance matrix,
    creates a text file listing the k-th nearest neighbors desired, and a unique edge
    list usable in Denali format.
    '''


    def __init__(self, treeFile, distanceFile="", gtp_path='gtp.jar'):
        '''
        Constructor
        '''
        self = self
        self.treeFile = treeFile
        self.distanceFile = distanceFile
        self.gtp_path = gtp_path
    
    
    def geoConvert(self):
        print "Feeding trees into GTP"
        #if not os.path.exists(self.distanceFile):
        infile = self.treeFile
        command = "java -jar " + self.gtp_path + " -u " + infile
        subprocess.call(command.split())
    
    
    def nearestNeighbors(self, treeName, treeNum=3, k=1):
        infile = open(self.distanceFile,'r')
        neighfile = open(treeName+'_raw_neighbors.txt','w')
        
        # process each line
        data = [line.rstrip('\n') for line in infile]
        infile.close()
        
        # construct list of k smallest neighbors
        # each separate line is treated as the appropriate first number of
        # a vertex pair
        vertex_counter = 0
        for eachLine in data:
            # convert the string line into a list of floats
            tempStrList = eachLine.split()
            tempData = []
            for i in xrange(len(tempStrList)):
                tempData.append(float(tempStrList[i]))
            # create a list of paired vertices and distances
            tupleList = []
            for i in range(len(tempData)):
                tupleList.append((i,tempData[i]))
                              
            # sort the list 
            tupleSorted = sorted(tupleList, key=lambda item: (item[1]))
            tupleIndices = [str(x[0]) for x in tupleSorted]
            # the first k items AFTER the zero (from diagonal) are the nearest neighbors
            kneighbors = str(vertex_counter) + "\t"
            for i in range(1, k+1):
                kneighbors = kneighbors + tupleIndices[i] + "\t"
            # write the list to a file 
            neighfile.write(kneighbors + "\n")
            vertex_counter = vertex_counter + 1
        neighfile.close()
        
    def graph_from_NN(self,treeName,treeNum):
        
        infile = open(treeName+'_raw_neighbors.txt','r')
        outfile = open(treeName+'_edges.txt','w')
        adjGraph = nx.Graph()
        for i in range(treeNum + 1):
            adjGraph.add_node(i)
        for eachLine in infile:
            tempLine = [int(t) for t in eachLine.split()]
            for i in range(1,len(tempLine)):
                adjGraph.add_edge(tempLine[0],tempLine[i])
        infile.close()
        edgelist = adjGraph.edges()
        for i in range(len(edgelist)):
            if (str(edgelist[i][0]) != str(edgelist[i][1])):
                outfile.write(str(edgelist[i][0]) + "\t"  + str(edgelist[i][1]) + "\n")
        outfile.close()
        vertfile = open(treeName+'_vertices.txt','w')
        likelihoodfile = open(treeName+'out.txt','r')
        for line in likelihoodfile:
            temp = line.split()
            vertfile.write(temp[1] + "\n")
        vertfile.close()
        likelihoodfile.close()
        
    
      
    #get_diss_matrix method by Megan A. Owen from helper scripts
    # Reads in the raw output of GTP (or the two file version)
    # and creates a dissimilarity matrix file of the distances.
    # Arguments: raw distance file output from GTP
    #            output file
    #            "symmetric" or "non" : whether matrix should be symmetric or not
    # Returns:  nothing (writes to output file)
    
 
    
       
  
    def get_diss_matrix(self, geo_file_name,diss_file_name,sym_flag):
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
    