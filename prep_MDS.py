'''
Created on Jun 25, 2015

@author: alkpongsema
'''
import os
from subprocess import call
from SequenceGenerator import *
from BayesExtract import *
from my_helper import *
import shutil
from make_rMDSscript import make_rMDSscript

if __name__ == '__main__':
    tree = ""
    #tree = "basenew" + "_raxml"
    tree_data = "\\" + tree
    seq_dir = 'c:\\seqgen\\'
    seq_tree_dir = 'c:\\seqgen\\' + tree + '\\'
    bayes_exe = 'mrbayes_x64.exe'
    
    
    if not os.path.exists(seq_dir + tree + "\\" + tree + ".nex"):
        tree_gen = SequenceGenerator(tree,"c:\\seqgen\\" + tree + ".txt")
        tree_gen.runseq_gen()
    else:
        print("SeqGen already run - skipping sequence generation.")
    
    # add code to move Mr. Bayes to the new SeqDir
    
    # create Mr. Bayes driver
    
    if not os.path.exists(seq_dir + tree + "\\" + tree + "-command.nex"):
        outfile = open(seq_tree_dir + tree + "-command.nex",'w')
        outfile.write("#NEXUS\n")
        outfile.write("\n")
        outfile.write("begin mrbayes;\n")
        outfile.write("\t" + "set autoclose=yes nowarn=yes;\n")
        outfile.write("\t" + "execute " + tree + ".nex;\n")
        outfile.write("\t" + "lset nst=6 rates=invgamma;\n")
        outfile.write("\t" + "mcmc ngen=5000000 samplefreq=1000;\n")
        outfile.write("\t" + "sump;\n")
        outfile.write("\t" + "sumt;\n")
        outfile.write("\t" + "quit;\n")
        outfile.write("end;\n")
        outfile.close()
           
    else:
        print("Skipping Mr Bayes Driver generation - already done")
    
    # Run Mr. Bayes MCMC
    '''
    if not os.path.exists(seq_dir + tree + "\\" + tree + ".nex" + ".mcmc"):
        os.chdir(seq_tree_dir)
        command = bayes_exe + " " + tree + "-command.nex"
        call(command.split())
    else:
        print("Skipping Mr Bayes MCMC - already done")
    '''
       
    # Create Bayes treeout
    if not os.path.exists(seq_dir + tree + "\\" + tree + "treeout.txt"):
        os.chdir(seq_tree_dir)
        tree_extract = BayesExtract(tree,seq_tree_dir + tree + ".nex", seq_tree_dir,1000)
        tree_extract.treeMatch()
    '''
    
        
    # Run Raxml if needed with default GTR parameters
    rax_path = "c:/raxml"
    rax_ver = "raxmlHPC"
    raxml_dir = "/raxml"
    data_name = tree
    rax_treeout = tree + "treeout.txt"
    if not os.path.exists(raxml_dir):
        os.mkdir(raxml_dir)
        os.system('./' + rax_ver + ' -s ' + seq_dir + '/' + data_name + '/' + data_name + '.nex' + ' -n ' + data_name + ' -m GTRGAMMA -e 0.001 -f a -k -x 27362 -p 96618 -N 1000 -w ' + os.getcwd() + '/' + raxml_dir )
    '''

    
    # Split by topologies
    
    analysis_version = "analysis_140702.jar"
    trees_no_base = tree + "treeout.txt"
    trees_topo_file_name =  tree + "_tree_topo.txt"
    
    # Copy analysis.jar to the seq directory
    
    if not os.path.exists(trees_topo_file_name):
        os.chdir(seq_tree_dir)

        command = "java -jar " + analysis_version + " -a topology_count -o " + trees_topo_file_name + " " + trees_no_base
        call(command.split())
    else:
        print ("File %s already exists - skipping generating topology info about all means \n" % trees_topo_file_name)

    # Add base tree to trees file:
    os.chdir(seq_tree_dir)
    trees_file_name = trees_no_base
    
    
    infile1 = open(seq_tree_dir + trees_no_base,'r')
    infile2 = open(tree + ".txt",'r')
    outfile = open(seq_tree_dir + "temptrees.txt",'w')
    outfile.write(infile2.readline()+"\n")
    infile2.close()
    for line in infile1:
        outfile.write(line)
    infile1.close()
    outfile.close()
    shutil.copyfile("temptrees.txt",trees_file_name)
    
    tree_distances = tree + "_distances.txt"
    tree_dist_matrix = tree + "_distancematrix.txt"
    gtp_jar = "gtp.jar"
    
    # Copy gtp.jar to the seq directory
    
      
    
    
    '''
    # Use GTP to get geodesic distances and create distance matrix file
    if not os.path.exists(tree_distances):
        os.chdir(seq_tree_dir)
        command = "java -jar " + gtp_jar + " -u -o " + tree_distances + " " + trees_file_name 
        call(command.split())
    else:
        print ("Distance file already exists - skipping running Analysis")
    
    if not os.path.exists(tree_dist_matrix):
        os.chdir(seq_tree_dir)
        get_diss_matrix(tree_distances,tree_dist_matrix,"symmetric")
    else:
        print ("Distance matrix already exists - skipping running Analysis")
    '''
    # Get RF distances
    
    if not os.path.exists(tree_distances):
        os.chdir(seq_tree_dir)
        command = "java -jar Distances_150624.jar -u -d RF -o " + tree_distances + " " + trees_file_name
    else:
        print("Distance file already exists")
    
    if not os.path.exists(tree_dist_matrix):
        os.chdir(seq_tree_dir)
        get_diss_matrix(tree_distances,tree_dist_matrix,"symmetric")
    else:
        print ("Distance matrix already exists - skipping running Analysis")    
    
    
    trees_mn_distances = tree + "_mn_distances.txt"
    trees_mn_dist_matrix = tree + "_mn_distmatrix.txt"
    trees_mean = tree + "_mean.txt"
    trees_and_mn = tree + "_mn_treeout.txt"
    
    
    # Find the mean tree
    sturm_version = "SturmMean_130704.jar"
    sturm_file = tree + "_sturm.txt"
    
    
    if not os.path.exists(sturm_file):
        os.chdir(seq_tree_dir)
        
        command = "java -jar " + sturm_version + " -a random -e 0.0001 -o " + sturm_file + " " + trees_file_name
        call(command.split())
    else:
        print("Mean already found - skipping SturmMean")
    
    # Extract the mean tree from the mean file
    # From my_helper
    
    if not os.path.exists(trees_mean):
        os.chdir(seq_tree_dir)
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
            print ("Warning: could not extract tree from the output file " + trees_mean + "; returning empty string")
    
    
    # Make the tree file including the mean:
    
    if not os.path.exists(trees_and_mn):
        
        infile1 = open(trees_file_name,'r')
        infile2 = open(trees_mean,'r')
        outfile = open(trees_and_mn,'w')
        outfile.write(infile2.readline())
        for line in infile1:
            outfile.write(line)
        infile1.close()
        infile2.close()
        outfile.close()

    # Use GTP to get geodesic distances and create distance matrix file for the mean and all trees:
     
    if not os.path.exists(trees_mn_distances):
        command = "java -jar " + gtp_jar + " -u -o " + trees_mn_distances + " " + trees_and_mn 
        call(command.split())
    else:
        print ("Distance file already exists for trees, base, and mean  - skipping running GTP")
    if not os.path.exists(trees_mn_dist_matrix):
        get_diss_matrix(trees_mn_distances,trees_mn_dist_matrix,"symmetric")
    else:
        print ("Distance matrix already exists for trees, base, and mean- skipping")
        
    
    
    trees_mn_maj_distances = tree + "_mn_maj_distances.txt"
    trees_mn_maj_dist_matrix = tree + "_mn_maj_distmatrix.txt"
    trees_and_mn_maj = tree + "_mn_maj_treeout.txt"
    trees_maj_file = tree + ".nex.con.tre"
    trees_maj = tree + "_maj.txt"
    
    # Make the tree file including the mean and majority trees:
    if not os.path.exists(trees_maj):
        # First, get taxa:
        infile = open(trees_maj_file,'r')
        taxa = []
        tree_line = ""
        for line in infile:
            temp = line.split()
            m = re.match('[0-9]+',temp[0])   # check for the labels
            if (m):
                taxa.append(temp[1].rstrip(',;'))
            elif (temp[0] == "tree"):
                tree_line = temp[4]
                break   # once we hit the tree portion of the nexus file, we're done
        infile.close()
        
        # Then, extract newick tree from the con_tree probability string:
        tree_sub = re.sub(r'\[.*?\]',"",tree_line)
        t_with_taxa = []
        for i in range(len(taxa)+1):
            for j in range(1,len(taxa)+1):
                tree_sub = re.sub(str(j)+':',taxa[j-1]+':',tree_sub)
        outfile = open(trees_maj,'w')
        outfile.write(tree_sub)
        outfile.close()    
    else:
        print("Majority tree already extracted from .con.tre - skipping")
        
    if not os.path.exists(trees_and_mn_maj):
        infile1 = open(trees_and_mn, 'r')
        infile2 = open(trees_maj, 'r')
        infile3 = open(trees_file_name,'r')
        outfile = open(trees_and_mn_maj, 'w')
        outfile.write(infile1.readline() + "\n")
        infile1.close()
        outfile.write(infile2.readline() + "\n")
        infile2.close()
        for line in infile3:
            outfile.write(line)
        infile3.close()
        outfile.close()
    else:
        print("Tree file plus base first mean second majority tree third already created - skipping")
    
       
    # Use GTP to get geodesic distances and create distance matrix file for the mean and all trees:
    
    
    if not os.path.exists(trees_mn_maj_distances):
        command = "java -jar " + gtp_jar + " -u -o " + trees_mn_maj_distances + " " + trees_and_mn_maj 
        call(command.split())
    else:
        print ("Distance file already exists for base mean maj - skipping running GTP")
    if not os.path.exists(trees_mn_maj_dist_matrix):
        get_diss_matrix(trees_mn_maj_distances,trees_mn_maj_dist_matrix,"symmetric")
    else:
        print ("Distance matrix already exists for base mean maj- skipping")
        
       
    # Create R script for MDS
    # Part one: geodesic
    
    # 2D:
    
    if not os.path.exists(tree + "_2D.r"):
        all_trees = make_rMDSscript(tree, tree_dist_matrix, "All trees and base tree under MDS", 1)
        all_trees.plot_MDS(2)
        command = "rscript " + tree + "_2D.r"
        call(command.split())
    else:
        print ("MDS plots already exist for 2D trees - skipping")
        
    # Second, all trees with the mean:
    if not os.path.exists(tree + "_mean" + "_2D.r"):
        all_trees_and_mean = make_rMDSscript(tree, trees_mn_dist_matrix, "All trees, base tree, and mean tree under MDS",1,mean=True)
        all_trees_and_mean.plot_MDS(2)
        command = "rscript " + tree + "_mean" + "_2D.r"
        call(command.split())
    
    # Third, all trees with mean and majority:
    if not os.path.exists(tree + "_mean_maj" + "_2D.r"):
        all_trees_and_mean_majority = make_rMDSscript(tree, trees_mn_maj_dist_matrix, "All trees, base tree, mean tree, and majority tree under MDS",1,mean=True,majority=True)
        all_trees_and_mean_majority.plot_MDS(2)
        command = "rscript " + tree + "_mean_maj" + "_2D.r"
        call(command.split())    
    
    # 3D:
    if not os.path.exists(tree + "_3D.r"):
        all_trees = make_rMDSscript(tree, tree_dist_matrix, "All trees and base tree under MDS", 1)
        all_trees.plot_MDS(3)
        command = "rscript " + tree + "_3D.r"
        call(command.split())
    else:
        print ("MDS plots already exist for 3D trees - skipping")
        
    # Second, all trees with the mean:
    if not os.path.exists(tree + "_mean" + "_3D.r"):
        all_trees_and_mean = make_rMDSscript(tree, trees_mn_dist_matrix, "All trees, base tree, and mean tree under MDS",1,mean=True)
        all_trees_and_mean.plot_MDS(3)
        command = "rscript " + tree + "_mean" + "_3D.r"
        call(command.split())
    
    # Third, all trees with mean and majority:
    if not os.path.exists(tree + "_mean_maj" + "_3D.r"):
        all_trees_and_mean_majority = make_rMDSscript(tree, trees_mn_maj_dist_matrix, "All trees, base tree, mean tree, and majority tree under MDS",1,mean=True,majority=True)
        all_trees_and_mean_majority.plot_MDS(3)
        command = "rscript " + tree + "_mean_maj" + "_3D.r"
        call(command.split())
        
    
           
    