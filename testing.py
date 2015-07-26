'''
Created on Jun 5, 2015

@author: alkpongsema
'''

from BayestoDenali import *
from SequenceGenerator import *
import shutil
import GeoFeed



if __name__ == '__main__':
    
    # Set tree and edit Mr Bayes and SeqGen locations if needed
    tree = "baserescaled"
    tree_data = "\\" + tree
    bayes_exe = "c:\\mrbayes\\mrbayes_x64.exe "
    bayes_driver="c:\\SeqGen\\" + tree + "\\" + tree + "-command.nex"
    seq_exe_dir = "c:\\seqgen\\"
    seq_dir = "c:\\seqgen\\" + tree
    trees_file_name = tree + "treeout.txt"
    
    '''
    # Run Seq-Gen if needed with default GTR parameters
    if not os.path.exists(seq_dir + tree + "\\" + tree + ".nex"):
        tree_gen = SequenceGenerator(tree,"c:\\seqgen\\" + tree + ".txt")
        tree_gen.runseq_gen()
        
    # Note: need to put the nexus output of Seq-Gen into Mesquite to convert to Phylip format first.
    # Need to implement command-line Mesquite here, or split stuff up
    
    # Run Raxml if needed with default GTR parameters
    rax_path = "c:/raxml"
    rax_ver = "raxmlHPC"
    raxml_dir = "/raxml"
    data_name = tree
    rax_treeout = tree + "_raxmlout.txt"
    if not os.path.exists(raxml_dir):
        os.mkdir(raxml_dir)
        os.system('./' + rax_ver + ' -s ' + seq_dir + '/' + data_name + '/' + data_name + '.nex' + ' -n ' + data_name + ' -m GTRGAMMA -e 0.001 -f a -k -x 27362 -p 96618 -N 1000 -w ' + os.getcwd() + '/' + raxml_dir )
    
    # Merge raxml best tree file w/bootstrap files
    # right now, leaving the 'best tree' out as it's misbehaving
    rax_treeout = tree + "_raxmlout.txt"
    
    if not os.path.exists(rax_treeout):
        rax_prefix = "RAxML_"
        #rax_best = rax_prefix + "bestTree." + tree + ".phy"
        rax_bootstrap = rax_prefix + "bootstrap." + tree
        #infile1 = open(rax_best,'r')
        infile2 = open(rax_bootstrap,'r')
        outfile = open(tree + "_raxmlout.txt",'w')
        #outfile.write(infile1.readline())
        #infile1.close()
        for line in infile2:
            outfile.write(line)
        infile2.close()
        outfile.close()
        
    else:
        print ("Skipping Raxml tree file combination - already done.")
    
    
    
    
    
    # Run Mr. Bayes if needed with default GTR parameters
    if not os.path.exists(seq_dir + "\\" + tree + ".nex.mcmc"):
        os.chdir(seq_dir)
        os.system(bayes_exe + bayes_driver)
    else:
        print "Skipping Mr. Bayes run - already done"
    
    # Extract files for GTP use
    if not os.path.exists(seq_dir + trees_file_name):
        newbase_extract = BayesExtract(tree,seq_dir + tree_data + ".nex",seq_dir + "\\",1000)
        newbase_extract.treeMatch()
    else:
        print "Skipping Bayes Extraction - already done"
    '''
    
      
    # output file
    
    analysis_version = "analysis_140702.jar"
    
    trees_topo_file_name =  tree + "_tree_topo.txt"
    #trees_file_name = rax_treeout
    
    # Get topology information about the tree file.
    if not os.path.exists(trees_topo_file_name):
            
            command = "java -jar " + analysis_version + " -a topology_count -o " + trees_topo_file_name + " " + trees_file_name
            call(command.split())
    else:
        print "File %s already exists - skipping generating topology info about all means \n" % trees_topo_file_name

    # 

    
    
    
    
    
    '''
    #Denali testing 
    
    if not os.path.exists(seq_dir + "newbasetreeout.txt"):
        base_extract = BayesExtract("newbase","c:\\seqgen\\newbase\\newbase.nex","c:\\seqgen\\newbase\\",50,25)
    else:
        print "Skipping Bayes Extraction - already done"
    
    if not os.path.exists(seq_dir + "newbase_vertices.txt"):
        newbase = BayestoDenali("newbase",seq_dir)
        newbase.converttoDenali()
        newbase.create_contour_tree(50,25)
    else:
        print "Skipping conversion to vertex, edge, and contour tree files for Denali - already done"
    
    '''
    
    
    