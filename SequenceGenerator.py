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


    def __init__(self, tree_name, newick_tree_file, seq_dir="c:\\seqgen"):
        '''
        Constructor
        '''
        self = self
        self.tree_name = tree_name
        self.newick = newick_tree_file
        self.seq_dir = seq_dir
        self.seq_outdir = seq_dir + "\\" + tree_name + "\\"
        self.seq_out = self.seq_outdir + tree_name + ".nex"
    
    def runseq_gen(self):
        
        if not os.path.exists(self.seq_outdir):
            os.mkdir(self.seq_outdir)
            os.system(self.seq_dir + '\\seq-gen ' + '-mGTR' +' -i0.18 ' + '-f0.21,0.31,0.3,0.18 ' + '-r1.5,4.91,1.34,0.83,5.8,1.0 ' + '-on ' + self.newick + ' > ' +  self.seq_out) 
            #call(command.split())
        else:
            print "Sequence file already generated - skipping SeqGen run."
        