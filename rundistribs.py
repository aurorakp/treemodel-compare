'''

Created July 1, 2015
 
'''

import shutil
from SequenceGenerator import *
from BayesExtract import *
from BEASTExtract import *
from my_helper import get_diss_matrix
from make_rMDSscript import make_rMDSscript
import os
import topology_file_splitter
from distribcompare import distribcompare
from LogMapPlotter import LogMapPlotter
import subprocess
from plot_topos import plot_topos
from operator import itemgetter
from plot_orderedlog import plot_orderedlog

def makeSeq(n,tree):
    seq_dir = 'c:\\seqgen\\'
    seq_tree_dir = 'c:\\seqgen\\' + tree + '\\'
    for i in range(1,n+1):
        shutil.copyfile(seq_dir + tree + ".txt", seq_dir + tree + str(i) + ".txt")
        if not os.path.exists(seq_dir + tree + "\\" + tree + str(i) +  ".nex"):
            tree_gen = SequenceGenerator(tree + str(i),"c:\\seqgen\\" + tree + str(i) +  ".txt")
            tree_gen.runseq_gen()
            shutil.copyfile(seq_dir + tree + str(i) + ".txt", seq_dir + tree + str(i) + "\\" + tree + str(i) + ".txt")
        else:
            print("SeqGen already run for tree " + str(i) + " - skipping sequence generation.")

def copyBayes(tree,treehome):
    bayes_home = 'c:\\seqgen\\bayesfiles\\'
    bayes_dir = treehome + "\\bayes\\"
    if not os.path.exists(bayes_dir):
        shutil.copytree(bayes_home, bayes_dir)
    else:
        print("Bayes files already copied for " + tree)

def copyTree(tree,treehome,targetdir):
    if not os.path.exists(targetdir + "\\" + tree):
        shutil.copyfile(treehome + tree + ".txt",targetdir + tree + ".txt")
        shutil.copyfile(treehome + tree + ".nex",targetdir + tree + ".nex")
    else:
        print("Tree and NEXUS files already copied for " + tree)
        
def makeBayesScript(tree,treedir):
    if not os.path.exists(treedir + "\\" + tree + "-command.nex"):
        outfile = open(treedir + tree + "-command.nex",'w')
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

def runBayes(tree,treedir):
    if not os.path.exists(treedir + "\\bayes\\" + tree + ".nex" + ".mcmc"):
        os.chdir(treedir + "\\bayes\\")
        command = "mrbayes_x64 " + tree + "-command.nex"
        call(command.split())
    else:
        print("Skipping Mr Bayes MCMC - already done for " + tree + ".")

def makeBayestreeouts(tree, treehome):
    if not os.path.exists(treehome + "\\" + tree + "_bayes_treeout.txt"):
        os.chdir(treehome)
        tree_extract = BayesExtract(tree, treehome + "\\" + tree + ".nex", treehome, 1000)
        tree_extract.treeMatch()
        trees_file_name = treehome  + tree + "_bayes_treeout.txt"
        shutil.copyfile(tree + "treeout.txt", trees_file_name)
    # Add the base tree in at line one:
        infile1 = open(trees_file_name,'r')
        infile2 = open(tree + ".txt",'r')
        outfile = open(treehome + "temptrees.txt",'w')
        outfile.write(infile2.readline()+"\n")
        infile2.close()
        for line in infile1:
            outfile.write(line)
        infile1.close()
        outfile.close()
        shutil.copyfile("temptrees.txt",trees_file_name)    
    
    else:
        print("Skipping Mr Bayes treeout extraction - already done for " + tree)

def copyGTP(treehome):
    gtp_version = "gtp.jar"
    if not os.path.exists(treehome + gtp_version):
        shutil.copyfile('c:\\seqgen\\jars\\' + gtp_version, treehome + gtp_version)

def findSturmMean(tree, treehome, model,rooted=False):   
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
        
    # Extract mean tree from file - from my_helper:
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

def extractMrBayesMajorityTree(tree, treehome):
    trees_maj = tree + "_bayes_maj.txt"
    trees_maj_file = tree + ".nex.con.tre"
    os.chdir(treehome)
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

def makeBayesMaj(tree, treehome):
    os.chdir(treehome + "/bayes/")
    treeout = tree + "treeout.txt"
    majout = tree + "_bayes_maj_treeout.txt"
    maj = tree + "_bayes_maj.txt"
    if not os.path.exists(majout):
        infile2 = open(maj, 'r')
        infile3 = open(treeout, 'r')
        outfile = open(majout, 'w')
        outfile.write(infile2.readline() + "\n")
        infile2.close()
        for line in infile3:
            outfile.write(line)
        infile3.close()
        outfile.close()
    else:
        print("Bayes treeout with mean and majority tree already extracted for " + tree + " - skipping")
        
def makeBayesMnMaj(tree, treehome):
    os.chdir(treehome)
    treeout = tree + "_bayes_treeout.txt"
    mnmajout = tree + "_bayes_mn_maj_treeout.txt"
    mn = tree + "_mn.txt"
    maj = tree + "_bayes_maj.txt"
    if not os.path.exists(mnmajout):
        infile1 = open(mn, 'r')
        infile2 = open(maj, 'r')
        infile3 = open(treeout, 'r')
        outfile = open(mnmajout, 'w')
        outfile.write(infile1.readline())
        infile1.close()
        outfile.write(infile2.readline() + "\n")
        infile2.close()
        for line in infile3:
            outfile.write(line)
        infile3.close()
        outfile.close()
    else:
        print("Bayes treeout with mean and majority tree already extracted for " + tree + " - skipping")

def plotMDS(tree, treehome, model, mn=False, maj=False):
    os.chdir(treehome)
    model_label = "_" + model + "_"
    titlest = "All trees with base "
    titleend = "under MDS"
    if (mn == True and maj == True):
        suffix = "_mn_maj_"
        titlest = titlest + " mean and majority trees "
    elif (mn == True):
        suffix = "_mn_"
        titlest = titlest + " and mean tree "
    else:
        suffix = "_"
        
    if not os.path.exists(tree + suffix + "2D.r"):
        temp = make_rMDSscript(tree, tree + model_label + "dist_matrix", titlest + titleend, 1, mn, maj)
        temp.plot_MDS(2)
        command = "rscript " + tree + "_2D.r"
        call(command.split())
    else:
        print ("MDS plots already exist for 2D trees - skipping")


def geoDistanceMatrix(tree, treefile, treehome, model, rooted=False):

    gtp_jar = "gtp.jar"
    model_label = "_" + model + "_"
    tree_distances = tree + model_label + "distances.txt"
    #print ("treehome is: " + treehome)
    #print ("tree distance file: " + tree_distances)
    #print ("treefile is: " + treefile)
    if not os.path.exists(tree_distances):
   
        if (rooted==False):
            command = "java -jar " + gtp_jar + " -u -o " + tree_distances + " " + treefile
 
        elif (rooted==True):
            command = "java -jar " + gtp_jar + " -o " + tree_distances + " " + treefile
        call(command.split())
    else:
        print ("Distance file already exists - skipping running Analysis")
        
    tree_dist_matrix = tree + model_label + "dist_matrix.txt"
    if not os.path.exists(tree_dist_matrix):
        get_diss_matrix(tree_distances,tree_dist_matrix,"symmetric")
    else:
        print ("Distance matrix already exists - skipping running Analysis")
        
def runRAxML(tree, treehome):
    rax_path = "c:\\raxml\\"
    rax_ver = "raxmlHPC"
    raxml_dir = "\\raxml"
    data_name = tree
    rax_treeout = tree + "_raxml_treeout.txt"
    
    print("Treehome is: " + treehome)

    if not os.path.exists(treehome + raxml_dir):
        print ("Treehome plus rax is: " + treehome + raxml_dir)
        os.chdir(treehome)
        #First, convert Nexus files to Phylip format:
        command = "convbioseq phylip " +  tree + ".nex"
        call(command.split())
        # Run RAxML:
        os.mkdir(treehome + "\\" + raxml_dir)
        os.system(rax_path + rax_ver + ' -s ' + treehome + '\\'  + data_name + '.phy' + ' -n ' + data_name + ' -m GTRGAMMA -e 0.001 -f a -k -x 27362 -p 96618 -N 1000 -w ' + os.getcwd() + raxml_dir + "\\" )
    else:
        print("RAxML directory already exists - skipping running RAxML")

def makeRAxMLtreeout(tree, treehome):
    outpath = treehome + "\\raxml\\" + tree + "_raxml_treeout.txt"
    print ('outpath is: ' + outpath)
    if not os.path.exists(outpath):
        os.chdir(treehome + "\\raxml\\")
        trees_file_name = treehome + "\\raxml\\" + tree +  "_raxml_treeout.txt"
        raxml_bootstrap = treehome  + "\\raxml\\" + "RAxML_bootstrap." + tree
        raxml_best = treehome + "\\raxml\\" +  "RAxML_bestTree." + tree   
    # Add the base tree in at line one:
        infile1 = open(treehome + "\\" + tree + ".txt",'r')
        infile2 = open(raxml_best,'r')
        infile3 = open(raxml_bootstrap,'r')
        outfile = open(trees_file_name,'w')
        outfile.write(infile1.readline()+"\n")
        outfile.write(infile2.readline())
        infile1.close()
        infile2.close()
        for line in infile3:
            outfile.write(line)
        infile3.close()
        outfile.close()
        findSturmMean(tree, treehome + "\\raxml\\","raxml")
    # Add the mean tree to the treeout file:
        mn = treehome + "\\raxml\\" + tree + "_mn.txt"        
        infile4 = open(outpath,'r')
        infile5 = open(mn,'r')
        outfile2 = open('temp.txt','w')
        outfile2.write(infile4.readline())
        outfile2.write(infile5.readline())
        for line in infile4:
            outfile2.write(line)
        infile4.close()
        infile5.close()
        outfile2.close()
        shutil.copy('temp.txt',outpath)
    else:
        print("Skipping RAxML treeout extraction - already done for " + tree)
        
def makeRAxMLbesttreeout(tree, treehome):
    outpath = treehome + "\\raxml\\" + tree + "_raxml_best_treeout.txt"
    if not os.path.exists(outpath):
        os.chdir(treehome + "\\raxml\\")
        trees_file_name = treehome + "\\raxml\\" + tree +  "_raxml_best_treeout.txt"
        raxml_bootstrap = treehome  + "\\raxml\\" + "RAxML_bootstrap." + tree
        raxml_best = treehome + "\\raxml\\" +  "RAxML_bestTree." + tree   
        infile2 = open(raxml_best,'r')
        infile3 = open(raxml_bootstrap,'r')
        outfile = open(trees_file_name,'w')
        outfile.write(infile2.readline())
        infile2.close()
        for line in infile3:
            outfile.write(line)
        infile3.close()
        outfile.close()
        
    else:
        print("Skipping RAxML best tree treeout extraction - already done for " + tree)
        
def prepforBEAUti(tree, treehome):
    beast_dir = "\\BEAST\\"
    if not os.path.exists(treehome + beast_dir):
        os.chdir(treehome)
        os.mkdir(treehome + beast_dir)
        shutil.copy(treehome + "\\" +  tree + ".nex", treehome + beast_dir + tree + ".nex")
        shutil.copy(treehome + "\\" +  tree + ".xml", treehome + beast_dir + tree + ".xml")
        shutil.copy(treehome + "\\" +  tree + "_state.xml", treehome + beast_dir + tree + "_state.xml")
    else:
        print("BEAST directory already exists - skipping for BEAUti prep for " + tree)
        
def runBEAST(tree, treehome):
    beast_dir = "\\BEAST\\"
    beast_path = "c:\\BEAST\\lib\\"
    beast_ver = "beast.jar"
    data_name = tree
    beast_rawout = tree + ".trees"
    beauti_out = tree + ".xml"
    state_file = tree + "_state.xml"


    if not os.path.exists(treehome + beast_dir + beast_rawout):
        print ("Treehome plus beast is: " + treehome + beast_dir)
        os.chdir(treehome + beast_dir)
        os.system("java -jar " + beast_path + beast_ver + " -beagle -working -seed 777 -statefile " + state_file + " " + beauti_out)
    else:
        print("BEAST directory already exists - skipping running BEAST")
        
def findBEASTbesttree(tree, treehome):
    # Tree Annotator
    beast_dir = "\\BEAST\\"
    beast_path = "c:\\BEAST\\"
    treeanno_ver = "treeannotator"
    beast_best = tree + "_maj"
    beast_rawout = tree + ".trees"
    burnin = 25
    
    if not os.path.exists(treehome + beast_dir + beast_best):
        out_temp = open(treehome + beast_dir + beast_best,'w')
        out_temp.write("")
        out_temp.close()
        command =  beast_path + treeanno_ver + " -burnin " + str(burnin) + " " + treehome + beast_dir + tree + ".trees " +  treehome + beast_dir + beast_best 
        call(command.split())
    else:
        print("Tree Annotator already run for " + tree + " - skipping")
    
    os.chdir(treehome + beast_dir)    
    trees_maj = tree + "_maj.txt"
    trees_maj_file = beast_best
    if not os.path.exists(trees_maj):
        # First, get taxa:
        infile = open(trees_maj_file,'r')
        print ("trees maj file is: " + trees_maj_file)
        taxa = []
        tree_line = ""
        for line in infile:
            temp = line.split()
            if (len(temp) == 0):
                continue
            else:
                m = re.match('[0-9]+',temp[0])   # check for the labels
                if (m):
                    taxa.append(temp[1].rstrip(',;'))
                elif (temp[0] == "tree"):
                    tree_line = temp[3]
                    break   # once we hit the tree portion of the nexus file, we're done
        print ("Taxa is: " + str(taxa))
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
        print("Majority tree already extracted from " + tree + ".trees - skipping")

def makeBeastTreeout(tree, treehome):
    beast_dir = "//BEAST//"
    beast_treeout = tree + "_BEAST_treeout.txt"
    if not os.path.exists(treehome + beast_dir + beast_treeout):
        temp = BEASTExtract(tree, tree + ".trees", treehome + beast_dir, 1000, 1)
        temp.treeMatch()
        os.chdir(treehome + beast_dir)
        infile1 = open(tree + "treeout.txt",'r')
        infile2 = open(treehome + "\\" + tree + ".txt",'r')
        outfile = open(beast_treeout,'w')
        outfile.write(infile2.readline()+ "\n")
        infile2.close()
        for line in infile1:
            outfile.write(line)
        infile1.close()
        outfile.close()
    else:
        print("Beast treeout already extracted from " + tree + ".trees - skipping")
        
def extractBEASTMaj (tree, treehome):
    os.chdir(treehome + "//BEAST//")
    treeout = tree + "_BEAST_treeout.txt"
    majout = tree + "_BEAST_maj_treeout.txt"
    maj = tree + "_maj.txt"
    if not os.path.exists(majout):
        infile2 = open(maj, 'r')
        infile3 = open(treeout, 'r')
        outfile = open(majout, 'w')
        outfile.write(infile2.readline() + "\n")
        infile2.close()
        for line in infile3:
            outfile.write(line)
        infile3.close()
        outfile.close()
    else:
        print("Beast treeout with majority tree already extracted for " + tree + " - skipping")
        
def extractBEASTMnMaj(tree, treehome):
    os.chdir(treehome + "//BEAST//")
    treeout = tree + "_BEAST_treeout.txt"
    mnmajout = tree + "_BEAST_mn_maj_treeout.txt"
    mn = tree + "_mn.txt"
    maj = tree + "_maj.txt"
    if not os.path.exists(mnmajout):
        infile1 = open(mn, 'r')
        infile2 = open(maj, 'r')
        infile3 = open(treeout, 'r')
        outfile = open(mnmajout, 'w')
        outfile.write(infile1.readline())
        infile1.close()
        outfile.write(infile2.readline() + "\n")
        infile2.close()
        for line in infile3:
            outfile.write(line)
        infile3.close()
        outfile.close()
    else:
        print("BEAST treeout with mean and majority tree already extracted for " + tree + " - skipping")

def treeout(tree, model, treehome):
    if (model == "bayes"):
        treeout = tree + "_bayes_maj_treeout.txt"
    elif (model == "BEAST"):
        shutil.copyfile(treehome + '/BEAST/' + tree + "treeout.txt", treehome + '/BEAST/' + tree + "BEASTtreeout.txt")
        treeout = tree + "_BEAST_maj_treeout.txt"
    elif (model == "raxml"):
        treeout = tree + "_raxml_best_treeout.txt"
    elif (model == "phyml"):
        treeout = tree + "_phyml_treeout.txt"
    return treeout

def createQQplots(tree, treehome, model1, model2,xlow=0,xhigh=1,ylow=0,yhigh=1):
    sturm_version = "SturmMean_130704.jar"
    analysis_jar = "analysis_140702.jar"
    shutil.copyfile('c:\\seqgen\\jars\\' + sturm_version, treehome + "\\" +  sturm_version)
    shutil.copyfile('c:\\seqgen\\jars\\' + analysis_jar, treehome + "\\" + analysis_jar)
    model1out = treeout(tree, model1, treehome)
    model2out = treeout(tree, model2, treehome)
    shutil.copyfile(treehome + '/' + model1 + '/' + model1out, treehome + '/' + model1out)
    shutil.copyfile(treehome + '/' + model2 + '/' + model2out, treehome + '/' + model2out)
    t1root = False
    t2root = False
    if (model1 == "BEAST"):
        t1root = True
        print "model1 is BEAST"
    if (model2 == "BEAST"):
        t2root = True
        print "model2 is BEAST"
    treeplot = distribcompare(tree + "_" + model1 + "_" + model2, model1out, model2out, treehome, t1root, t2root)
    treeplot.find_means()
    treeplot.find_disttomean()
    treeplot.set_dims(xlow,xhigh,ylow,yhigh)
    treeplot.qq_plot()

def runPhyML(tree, treehome):
    phyml_path = "c:\\phyml\\bin\\"
    phyml_ver = "phyml"
    phyml_dir = "\\phyml"
    phyml_name = tree
    
    
    print("Treehome is: " + treehome)

    if not os.path.exists(treehome + phyml_dir):
        print ("Treehome plus phyml is: " + treehome + phyml_dir)
        os.chdir(treehome)
        #First, convert Nexus files to Phylip format:
        command = "convbioseq phylip " +  tree + ".nex"
        call(command.split())
        #Run PhyML:
        os.mkdir(treehome + "\\" + phyml_dir)
        shutil.copy(treehome + "\\" + tree + ".phy",treehome + phyml_dir + "\\" + tree + ".phy")
        os.chdir(treehome + phyml_dir)
        os.system(phyml_path + phyml_ver + ' -i ' + tree + ".phy -b 1000 -c 4 -a e -m GTR -v e")
    else:
        print("PhyML directory already exists - skipping running PhyML")

def makePhyMLtreeout(tree, treehome):
    os.chdir(treehome + "\\phyml")
    infile1 = open(tree + ".phy" + "_phyml_tree.txt",'r')
    best_tree = re.sub(r'([0-9]+:)',":",infile1.readline())
    infile2 = open(tree + ".phy" + "_phyml_boot_trees.txt",'r')
    outfile = open(tree + "_phyml_treeout.txt",'w')
    outfile.write(best_tree)
    infile1.close()
    for line in infile2:
        outfile.write(line)
    infile2.close()
    outfile.close()
    
def orderByLogMap(tree, treehome, model):
    # Assumes you've already done the log map to generate 'all coordinates':
    all_coords_file = tree + "_" + model + "_allcoords.txt"
    ordered_coords_file = tree + "_" + model + "_ordered_allcoords.txt"
    ordered_trees_file = tree + "_" + model + "_ordered_treeout.txt"
    os.chdir(treehome + "/" + model + "/")
    infile1 = open(all_coords_file,'r')
    coords_y = []
    coords = []
    
    for line in infile1:
        coords.append(line.rstrip("/n"))
        temp = line.split(" ")
        coords_y.append(temp[1])
    infile1.close()
    
    # Sort the coordinates, keeping track of their index:
    coords_ordered = sorted((e,i) for i,e in enumerate(coords_y))
    
    # Import trees
    trees_raw = []
    infile2 = open(treehome + "/" + model + "/" + treeout(tree,model,treehome),'r')
    for line in infile2:
        temp = line.rstrip("\n")
        trees_raw.append(temp)
    infile2.close()
    
    # Sort the trees by the coordinates for use in MDS:
    trees_sorted = [None] * 1001
    #print("Trees_raw length is: " + str(len(trees_raw)) + " for model " + model)
    #print("Coords_ordered length is: " + str(len(coords_ordered)) + " for model " + model)
    for i in range(len(trees_raw)):
        trees_sorted[i] = trees_raw[coords_ordered[i][1]]
        
    coords_sorted = [None] * 1001
    # Sort the coordinates for logmap:
    for i in range(len(coords)):
        coords_sorted[i] = coords[coords_ordered[i][1]]
    
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

def convertRootedCoords(tree, treecoordsdir):
    coordsfiles = os.listdir(treecoordsdir)
    os.chdir(treecoordsdir)
    os.mkdir("origcoords")
    for coords_file_name in coordsfiles:
        shutil.copy(coords_file_name, treecoordsdir + "/origcoords/" + coords_file_name)
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
            
        
def lognormcoords(tree, treehome, model):
    coordsdir = treehome + "/" + model + "/coords/"
    coordsfiles = os.listdir(coordsdir)
    topodir = treehome + "/" + model + "/split_by_topology"
    topofiles = os.listdir(topodir)
    
    
    
        
if __name__ == '__main__':
    
    #tree = "onetenth"
    #tree = "ctwotenth"
    tree = "largeleaves"
    treedir = "c:/seqgen/" + tree
    '''
    model = 'BEAST'
    modeldir = '/BEAST/'
    #for i in range(1,2):
    #   convertRootedCoords(tree + str(i), treedir + str(i) + modeldir + 'coords/')
    
    
    # Make the Sequences
    makeSeq(10,tree)
    
    treedir = 'c:\\seqgen\\' + tree
    model = "bayes"
    bayesdir = "\\bayes\\"
    ### Section:  Mr Bayes###
    
    # Move Mr. Bayes files and the sequence files to the appropriate directory
    for i in range(1,11):
        copyBayes(tree + str(i), treedir + str(i))
        copyTree(tree + str(i), treedir + str(i) + "\\",treedir + str(i) + "\\bayes\\")
    
    # Generate Mr. Bayes command scripts
    for i in range(1,11):
        makeBayesScript(tree + str(i), treedir + str(i) + "\\bayes\\")
        
    # Run Mr. Bayes MCMC:
    #for i in range(1,11):
    #    runBayes(tree + str(i), treedir + str(i))
    
    # Extract trees:
    for i in range(1,11):
        makeBayestreeouts(tree + str(i), treedir + str(i) + "\\bayes\\")
        findSturmMean(tree + str(i), treedir + str(i) + "\\bayes\\","bayes")
        extractMrBayesMajorityTree(tree + str(i), treedir + str(i) + "\\bayes\\")
        makeBayesMnMaj(tree + str(i), treedir + str(i) + "\\bayes\\")
        
    # Find geodesic distances:
    for i in range(1,11):
        #print("Target path is: " + treedir + str(i) + "\\bayes\\")
        copyGTP(treedir + str(i) + "\\bayes\\")
        # Base + all trees
        geoDistanceMatrix(tree + str(i), tree + str(i) + "_" + model + "_treeout.txt", treedir + str(i) + bayesdir, model)
        # Base + mean and maj
        geoDistanceMatrix(tree + str(i), tree + str(i) + "_" + model + "_" + "mn_maj_treeout.txt" , treedir + str(i) + bayesdir, model)
    
    # Section: RAxML 
    
    # Run RAxML
    for i in range (1,11):
        runRAxML(tree + str(i), treedir + str(i))
        makeRAxMLtreeout(tree + str(i), treedir + str(i))
        findSturmMean(tree + str(i), treedir + str(i) + "\\raxml\\","raxml")
        
    
    # Find geodesic distances:    
    model = "raxml"
    raxdir = "\\raxml\\"
    for i in range(1,11):
        print("Target path is: " + treedir + str(i) + raxdir)
        copyGTP(treedir + str(i) + raxdir)
        # Base + best + all bootstrap trees
        geoDistanceMatrix(tree + str(i), tree + str(i) + "_" + model + "_" + "treeout.txt" , treedir + str(i) + raxdir, model)
    
    
    # BEAST section
    
    # Prep for BEAUti - need to figure out command line way to do this
    
    # Run BEAST routines:
    
    for i in range(1,11):
        model = "BEAST"
        prepforBEAUti(tree + str(i), treedir + str(i))
        runBEAST(tree + str(i), treedir+ str(i))
        findBEASTbesttree(tree+ str(i), treedir + str(i))
        makeBeastTreeout(tree + str(i), treedir + str(i))
        findSturmMean(tree + str(i), treedir + str(i) + "\\BEAST\\","BEAST",rooted=True)
        extractBEASTMnMaj(tree + str(i), treedir + str(i))
    
    # Find geodesic distances:
        beast_dir = "\\BEAST\\"
    for i in range(1,11):
        copyGTP(treedir + str(i) + beast_dir)
        # Base + mean + majority + other 1000 trees
        geoDistanceMatrix(tree + str(i), tree + str(i) + "_" + model + "_" + "treeout.txt" , treedir + str(i) + beast_dir, model,rooted=True)
    
    
    #PhyML
    for i in range(1,11):
        runPhyML(tree + str(i), treedir + str(i))
        makePhyMLtreeout(tree + str(i), treedir + str(i))
        findSturmMean(tree + str(i), treedir + str(i) + "\\phyml\\","phyml")
        
    
        # Find geodesic distances:    
        model = "phyml"
        phyml_dir = "\\phyml\\"
        print("Target path is: " + treedir + str(i) + phyml_dir)
        copyGTP(treedir + str(i) + phyml_dir)
        # Base + best + all bootstrap trees
        geoDistanceMatrix(tree + str(i), tree + str(i) + "_" + model + "_" + "treeout.txt" , treedir + str(i) + phyml_dir, model)
    
    
    
    ### Plotting Section
    models = ["bayes","raxml","BEAST","phyml"]
    
    #for j in range(len(models)):
    #   model = models[j]
    #   for i in range(1,11):
            
    #       treedir = "c:/seqgen/" + tree
    #       model_dir = "/" + model + "/"
    #       topo_dir = "split_by_topology/"
    #       if os.path.exists(treedir + str(i) + model_dir + topo_dir):
    #           shutil.rmtree(treedir + str(i) + model_dir + topo_dir)
    
    #    Adding coloring:
    # Need:
    # 1) Logmap ordered trees
    # 1)a) Plot logmap ordered trees
    # 2) Feed trees into distance file
    # 3) Create new distance matrix
    # 4) Run MDS
    #models = ["bayes","raxml","BEAST","phyml"]
    models = ["bayes","raxml"]
    
    models = ['BEAST']
    for j in range(len(models)):
        model = models[j]
        treedir = 'c:/seqgen/' + tree
        
        for i in range (1,2):
            
            
            analysis_version = "analysis_140702.jar"
            treedir = 'c:/seqgen/' + tree
            model_dir = '/' + model + '/'
            makeBayesMaj(tree + str(i), treedir + str(i))
            makeRAxMLbesttreeout(tree + str(i), treedir + str(i))
            topo_dir = treedir + str(i) + model_dir + 'split_by_topology'
            topo_prefix = topo_dir + "/topo.txt"
            centre_dir = treedir + str(i) + model_dir + 'centres'
            centre_prefix = centre_dir + "/centre_"
            trees_topo_file_name = treedir + str(i) + model_dir + tree + str(i) + "_" + model + "_tree_topo.txt"
            
            trees_file_name = treeout(tree + str(i), model, treedir + str(i))
            #print ("trees file is: " + trees_file_name)
            
        
            
            all_topos_coords_centre1 = tree + str(i) + "_" + model + "_allcoords.txt"   
            if not os.path.exists(treedir + str(i) + model_dir + all_topos_coords_centre1):
                    os.chdir(treedir + str(i) + model_dir)
                    if (model == 'BEAST'):
                        command = 'java -jar ' + analysis_version + ' -a log_map -o ' + all_topos_coords_centre1 + ' -f ' + centre_prefix + "1" + ' ' + treedir + str(i) + model_dir + trees_file_name
                    else:
                        command = 'java -jar ' + analysis_version + ' -u -a log_map -o ' + all_topos_coords_centre1 + ' -f ' + centre_prefix + "1" + ' ' + treedir + str(i) + model_dir + trees_file_name
                        print(command + "\n")
                    subprocess.call(command.split())
            
            orderByLogMap(tree + str(i), treedir + str(i), model)
            plotit = plot_orderedlog(tree + str(i), treedir + str(i), model)
            plotit.makeScript()
            plotit.makePlots()
            trees_ordered_file = tree + str(i) + "_" + model + "_ordered_treeout.txt"
            if (model == "BEAST"):
                os.chdir(treedir + str(i) + model_dir)
                geoDistanceMatrix(tree + str(i), trees_ordered_file, treedir + str(i) + model_dir, model, True)
            else:   
                os.chdir(treedir + str(i) + model_dir)
                geoDistanceMatrix(tree + str(i), trees_ordered_file, treedir + str(i) + model_dir, model, False)
            dist_matrix_file = tree + str(i) + "_" + model + "_" + "dist_matrix.txt"
            colMDS = make_rMDSscript(tree + str(i), treedir + str(i) + model_dir, dist_matrix_file, "Colored relative to Logmap order", aspect_ratio=1)
            colMDS.plot_MDS(2)
            colMDS.plot_MDS(3)    
            colMDS.run_MDSplots(2)
            colMDS.run_MDSplots(3)
            
            if not os.path.exists(trees_topo_file_name):    
                os.chdir(treedir + str(i) + model_dir)
                command = "java -jar " + analysis_version + " -a topology_count -o " + trees_topo_file_name + " " + trees_file_name
                subprocess.call(command.split())
            else:
                print "File %s already exists - skipping generating topology info about all means \n" % trees_topo_file_name
            if not os.path.exists(topo_dir):
                os.mkdir(topo_dir)
                topology_file_splitter.makeFiles(trees_file_name,trees_topo_file_name,topo_prefix)
            else:
                print "Directory %s already exists - skipping splitting the means by topology \n" % topo_dir
            
            centre_dir = treedir + str(i) + model_dir + 'centres'
            centre_prefix = centre_dir + "/centre_"
            topology_num = 0
            if not os.path.exists(centre_dir):
                os.mkdir(centre_dir)
                f = open(trees_topo_file_name)
                topNum = 0
                # Extract the number of topologies from the topology file
                for line in f:
                    tempStr = line
                    if (tempStr[0:3] != "Raw"):
                        continue
                    else: 
                        trimStr = tempStr.lstrip("Raw topology counts:  ").split()
                        topNum = len(trimStr)
                        topology_num = topNum
                        break
                f.close()
                
                
                for n in xrange(1,topNum+1):
                    
                    testout = centre_prefix + str(n)
                    tree_file_name = topo_dir + '/topo' + str(n) + '.txt'
                    f = open(tree_file_name,'r')
                    temptree = f.readline()
                    if (temptree == "(((E:.1,D:.1):.1,C:.11):.01,B:.1,A:.1);\n"):
                        temptree = "(((E:0.1,D:0.1):0.1,C:0.11):0.01,B:0.1,A:0.01);\n"
                    if (model == "BEAST" and temptree != "(((E:0.1,D:0.1):0.1,C:0.11):0.01,B:0.1,A:0.01);\n"):
                        m = re.match(r'(.*?\):)[0-9]+[.][0-9]+(.*?\):)[0-9]+[.][0-9]+(.*?\):)[0-9]+[.][0-9]+(.+;)',temptree)
                    else:
                        m = re.match(r'(.*?\):)[0-9]+[.][0-9]+(.*?\):)[0-9]+[.][0-9]+(.+;)',temptree)
                    if not m:
                        print("Error:  can't change interior edges lengths")
                        exit
                    if (model == "BEAST" and temptree != "(((E:0.1,D:0.1):0.1,C:0.11):0.01,B:0.1,A:0.01);\n"):
                        temptree = m.group(1) + '0.000000001' + m.group(2) + '0.000000001' + m.group(3) + '0.000000001' + m.group(4)
                    else:
                        temptree = m.group(1) + '0.000000001' + m.group(2) + '0.000000001' + m.group(3)
                    out = open(centre_prefix + str(n),'w')
                    out.write(temptree + '\n')
                    out.close()
                    f.close()
                       
            coords_dir = treedir + str(i) + model_dir + 'coords'
            coords_prefix = coords_dir + "/coords_"
            if not os.path.exists(coords_dir):
                os.mkdir(coords_dir)
                for topo_file_name in os.listdir(topo_dir):
                    # get the number at the end of the file name
                    match_file_name = re.match(r'topo([0-9]+).txt',topo_file_name)
                    z = int(match_file_name.group(1))
                    if (model == "BEAST"):
                        command = 'java -jar ' + treedir + str(i) + "/" + analysis_version + ' -a log_map -o ' + coords_prefix + str(z) + '.txt -f ' + centre_prefix + str(z) + ' ' + topo_dir +'/' +topo_file_name
                    else:
                        command = 'java -jar ' + treedir + str(i) + "/" +analysis_version + ' -u -a log_map -o ' + coords_prefix + str(z) + '.txt -f ' + centre_prefix + str(z) + ' ' + topo_dir +'/' +topo_file_name
                    subprocess.call(command.split())
                    if (model == "BEAST"):
                        convertRootedCoords(tree + str(i), treedir + str(i) + model_dir + 'coords/')
            else:
                print "Directory %s already exists - skipping computing the log map coordinates \n" % coords_dir
            
            all_topos_coords_centre1 = tree + str(i) + "_allcoords.txt"   
            if not os.path.exists(all_topos_coords_centre1):
                    command = 'java -jar ' + analysis_version + ' -u -a log_map -o ' + all_topos_coords_centre1 + ' -f ' + centre_prefix + "1" + ' ' + trees_file_name
                    subprocess.call(command.split())
            
            plots_dir = treedir + str(i) + model_dir + 'quadrant_plots'
            treedir_full = treedir + str(i) + model_dir
            if not os.path.exists(plots_dir):
                os.mkdir(plots_dir)
                plotit = plot_topos(tree + str(i), treedir_full, model, topology_num)
                plotit.makeScript()
                plotit.makePlots()
            else:
                print ("Plots for quadrants already made - skipping for " + tree + str(i))
    
            #if not os.path.exists(treedir + str(i) + 'quadrant_plots/' + tree + str(i) + '_' + model + '_' + "logplots.R"):
                #orderByLogMap(tree + str(i), treedir + str(i), model)
                #plotlog = plot_orderedlog(tree + str(i), treedir_full, model)
                #plotlog.makeScript()
                #plotlog.makePlots()
        
    
    for j in range(len(models)):
        model = models[j]
        for i in range(1,2):
            treedir = "c:/seqgen/" + tree
            model_dir = "/" + model + "/"
            dist_matrix_file = tree + str(i) + "_" + model + "_" + "dist_matrix.txt"
            # MDS (2D):
            if not os.path.exists(treedir + str(i) + model_dir + tree + str(i) + "_2D.r"):  
                temp = make_rMDSscript(tree + str(i), treedir + str(i) + model_dir, dist_matrix_file, model + ": sequence # " + str(i) + " under MDS", aspect_ratio=1, mean=False, majority=False)
                temp.plot_MDS()
            
                os.chdir(treedir + str(i) + model_dir)
                command = 'C:\\Rstuff\\R-3.2.0\\bin\\Rscript.exe ' + treedir + str(i) + model_dir + tree + str(i) + "_2D.r"
                call(command.split())
            else:
                print("R script and plots already made for " + tree + str(i) + " under model " + model + " - skipping")
            # MDS (3D):   
            if not os.path.exists(treedir + str(i) + model_dir + tree + str(i) + "_3D.r"):  
                temp = make_rMDSscript(tree + str(i), treedir + str(i) + model_dir, dist_matrix_file, model + ": sequence # " + str(i) + " under MDS", aspect_ratio=1, mean=False, majority=False)
                temp.plot_MDS(3)
            
                os.chdir(treedir + str(i) + model_dir)
                command = 'C:\\Rstuff\\R-3.2.0\\bin\\Rscript.exe ' + treedir + str(i) + model_dir + tree + str(i) + "_3D.r"
                call(command.split())
            else:
                print("R script and plots already made for " + tree + str(i) + " under model " + model + " - skipping")
            # Logmap:#
            analysis_jar = "analysis_140702.jar"
            shutil.copyfile('c:\\seqgen\\jars\\' + analysis_jar, treedir + str(i) + model_dir + analysis_jar)
            
    
    #models = ["bayes","raxml","BEAST","phyml"]
    
    for j in range(len(models)):
        model = models[j]
        for i in range (1,2):
            analysis_version = "analysis_140702.jar"
            treedir = 'c:/seqgen/' + tree
            model_dir = '/' + model + '/'
            topo_dir = treedir + str(i) + model_dir + 'split_by_topology'
            trees_file_name = treedir + str(i) + model_dir + tree + str(i) + "_" + model + "_" + "treeout.txt"
            trees_topo_file_name = treedir + str(i) + model_dir + tree + str(i) + "_" + model + "_tree_topo.txt"
            topo_prefix = topo_dir + "/topo.txt"
            if not os.path.exists(trees_topo_file_name):
                os.chdir(treedir + str(i) + model_dir)
                command = "java -jar " + analysis_version + " -a topology_count -o " + trees_topo_file_name + " " + trees_file_name
                subprocess.call(command.split())
            else:
                print "File %s already exists - skipping generating topology info about all means \n" % trees_topo_file_name
            if not os.path.exists(topo_dir):
                os.mkdir(topo_dir)
                topology_file_splitter.makeFiles(trees_file_name,trees_topo_file_name,topo_prefix)
            else:
                print "Directory %s already exists - skipping splitting the means by topology \n" % topo_dir
            
            centre_dir = treedir + str(i) + model_dir + 'centres'
            centre_prefix = centre_dir + "/centre_"
            topology_num = 0
            if not os.path.exists(centre_dir):
                os.mkdir(centre_dir)
                f = open(trees_topo_file_name)
                topNum = 0
                # Extract the number of topologies from the topology file
                for line in f:
                    tempStr = line
                    if (tempStr[0:3] != "Raw"):
                        continue
                    else: 
                        trimStr = tempStr.lstrip("Raw topology counts:  ").split()
                        topNum = len(trimStr)
                        topology_num = topNum
                        break
                f.close()
                
                
                for n in xrange(1,topNum+1):
                    
                    testout = centre_prefix + str(n)
                    tree_file_name = topo_dir + '/topo' + str(n) + '.txt'
                    f = open(tree_file_name,'r')
                    temptree = f.readline()
                    if (temptree == "(((E:.1,D:.1):.1,C:.11):.01,B:.1,A:.1);\n"):
                        temptree = "(((E:0.1,D:0.1):0.1,C:0.11):0.01,B:0.1,A:0.01);\n"
                    if (model =="BEAST"):
                        m = re.match(r'(.*?\):)[0-9]+[.][0-9]+(.*?\):)[0-9]+[.][0-9]+(.*?\):)[0-9]+[.][0-9]+(.+;)',temptree)
                    else:
                        m = re.match(r'(.*?\):)[0-9]+[.][0-9]+(.*?\):)[0-9]+[.][0-9]+(.+;)',temptree)
                    if not m:
                        print("Error:  can't change interior edges lengths")
                        exit
                    if (model =="BEAST"):
                        temptree = m.group(1) + '0.000000001' + m.group(2) + '0.000000001' + m.group(3)
                    else:
                        temptree = m.group(1) + '0.000000001' + m.group(2) + '0.000000001' + m.group(3) + '0.000000001' + m.group(4)
                    out = open(centre_prefix + str(n),'w')
                    out.write(temptree + '\n')
                    out.close()
                    f.close()
                       
            coords_dir = treedir + str(i) + model_dir + 'coords'
            coords_prefix = coords_dir + "/coords_"
            if not os.path.exists(coords_dir):
                os.mkdir(coords_dir)
                for topo_file_name in os.listdir(topo_dir):
                    # get the number at the end of the file name
                    match_file_name = re.match(r'topo([0-9]+).txt',topo_file_name)
                    z = int(match_file_name.group(1))
                    command = 'java -jar ' + analysis_version + ' -u -a log_map -o ' + coords_prefix + str(z) + '.txt -f ' + centre_prefix + str(z) + ' ' + topo_dir +'/' +topo_file_name
                    subprocess.call(command.split())
            else:
                print "Directory %s already exists - skipping computing the log map coordinates \n" % coords_dir
            
            all_topos_coords_centre1 = tree + str(i) + "_allcoords.txt"   
            if not os.path.exists(all_topos_coords_centre1):
                    command = 'java -jar ' + analysis_version + ' -u -a log_map -o ' + all_topos_coords_centre1 + ' -f ' + centre_prefix + "1" + ' ' + trees_file_name
                    subprocess.call(command.split())
            
            plots_dir = treedir + str(i) + model_dir + 'quadrant_plots'
            treedir_full = treedir + str(i) + model_dir
            if not os.path.exists(plots_dir):
                os.mkdir(plots_dir)
                plotit = plot_topos(tree + str(i), treedir_full, model, topology_num)
                plotit.makeScript()
                plotit.makePlots()
            else:
                print ("Plots for quadrants already made - skipping for " + tree + str(i))
                
    
    
    for i in range (1,11):
        tree = "largeleaves"
        treedir = 'c:/seqgen/' + tree
        makeBayesMaj(tree + str(i), treedir + str(i))
        makeRAxMLbesttreeout(tree + str(i), treedir + str(i))
        extractBEASTMaj(tree + str(i), treedir + str(i))
    '''
    models = ["bayes","raxml","BEAST","phyml"]            
    for i in range(1,2):
        treedir = 'c:/seqgen/' + tree + str(i) 
        for j in range(len(models)):
            for k in range(len(models)):
                if not (j == k):
                    createQQplots(tree + str(i), treedir, models[j], models[k],0.0,0.1,0.0,0.1)
    
    