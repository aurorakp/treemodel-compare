'''
Created on Jun 10, 2015

@author: alkpongsema
'''

from subprocess import call
import os

class SequenceGenerator(object):
    '''
    This script is meant to automate Seq-Gen for tree evolution purposes
    '''


    def __init__(self, tree_name, newick_tree_file, seq_suffix="", evomodel = "GTR", seq_dir="c:\\seqgen"):
        '''
        Constructor
        '''
        self = self
        self.tree_name = tree_name
        self.newick = newick_tree_file
        self.seq_suffix = seq_suffix
        self.seq_dir = seq_dir
        self.seq_outdir = seq_dir + "\\" + tree_name + "\\"
        self.seq_out = self.seq_outdir + tree_name + seq_suffix + ".nex"
        self.evomodel = evomodel
    
    def runseq_gen(self):
        
        # Note - seq-gen parameters are taken from the median of those estimated by the four models for the original
        # seagrass data set.  
        
        if not os.path.exists(self.seq_outdir):
            os.mkdir(self.seq_outdir)
            #if (self.evomodel == "GTR"):
            os.system(self.seq_dir + '\\seq-gen ' + '-mGTR' +' -i0.2 ' + '-f0.21,0.31,0.3,0.18 ' + '-r1.5,4.91,1.34,0.83,5.8,1.0 ' + '-on ' + self.newick + ' > ' +  self.seq_out)
            #elif (self.evomodel == "K-80"): 
            #   os.system(self.seq_dir + '\\seq-gen ' + '-mHKY' +' -i0.2 ' + '-fe ' + '-t5.18 ' + '-on ' + self.newick + ' > ' +  self.seq_out)
            #call(command.split())
        else:
            print "Sequence file already generated - skipping SeqGen run."
        