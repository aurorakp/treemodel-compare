'''
Created on Apr 12, 2016

@author: alkpongsema
'''

import re
import scipy

class Euclidean(object):
    '''
    classdocs
    '''


    def __init__(self, tree1, tree2, taxaNum=5):
        '''
        Constructor
        '''
        self.tree1 = tree1
        self.tree2 = tree2
        self.edgeslist1
        self.leaflist1
        self.ordtreelist1
        self.edgeslist2
        self.leaflist2
        self.ordtreelist2
        
        self.populate_lists(tree1, tree2)
        
        
    def populate_lists(self, tree1, tree2):
        
        # Do tree 1:
        
        # First, check for format - if it uses scientific notation, we'll need to parse that with one regex.
        m = re.match(r':([0-9]+[.][0-9]+[e][-][0-9]+)',tree1)
        if m:
        
            rawlist = re.findall(r':([0-9]+[.][0-9]+[e][-][0-9]+)',tree1)
            self.edgeslist1 = re.findall(r'\):([0-9]+[.][0-9]+[e][-][0-9]+)', tree1)
            self.leaflist1 = [rawlist[i] for i in range(len(rawlist)) if rawlist[i] not in self.edgeslist1]
            self.ordtreelist1 = self.edgeslist1
            for j in range(len(self.leaflist1)):
                self.ordtreelist1.append(self.leaflist1[j])
                
        # If that one doesn't fit, try 'normal' numbers
        
        elif not m:
            m1 = re.match(r':([0-9]+[.][0-9]+)',tree1)
            if m1:
                rawlist = re.findall(r':([0-9]+[.][0-9]+)',tree1)
                self.edgeslist1 = re.findall(r'\):([0-9]+[.][0-9]+)',tree1)
                self.leaflist1 = [rawlist[i] for i in range(len(rawlist)) if rawlist[i] not in self.edgeslist1]
                self.ordtreelist1 = self.edgeslist2
                for j in range(len(self.leaflist1)):
                    self.ordtreelist1.append(self.leaflist1[j])
        
        # Repeat for tree 2
        m = re.match(r':([0-9]+[.][0-9]+[e][-][0-9]+)',tree2)
        if m:
        
            rawlist = re.findall(r':([0-9]+[.][0-9]+[e][-][0-9]+)',tree2)
            self.edgeslist2 = re.findall(r'\):([0-9]+[.][0-9]+[e][-][0-9]+)', tree2)
            self.leaflist2 = [rawlist[i] for i in range(len(rawlist)) if rawlist[i] not in self.edgeslist2]
            self.ordtreelist2 = self.edgeslist2
            for j in range(len(self.leaflist2)):
                self.ordtreelist1.append(self.leaflist2[j])
        elif not m:
            m1 = re.match(r':([0-9]+[.][0-9]+)',tree2)
            if m1:
                rawlist = re.findall(r':([0-9]+[.][0-9]+)',tree2)
                self.edgeslist2 = re.findall(r'\):([0-9]+[.][0-9]+)',tree2)
                self.leaflist2 = [rawlist[i] for i in range(len(rawlist)) if rawlist[i] not in self.edgeslist2]
                self.ordtreelist2 = self.edgeslist2
                for j in range(len(self.leaflist2)):
                    self.ordtreelist2.append(self.leaflist2[j])
                    
    def get_euclidDistance(self):
        dist = scipy.spatial.distance.euclidean_distance(self.ordtreelist1,self.ordtreelist2)
        return dist