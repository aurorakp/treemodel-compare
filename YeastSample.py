'''
Created on Aug 3, 2015

@author: alkpongsema
'''
from random import shuffle
from random import seed

class YeastSample(object):
    '''
    classdocs
    1. Loads in the Yeast file
    2. Loads in the gene labels
    
    '''


    def __init__(self, geneNum=1,basedir = "c:/seqgen"):
        '''
        
        '''
        self.yeastFile = "All_genes_charsets_nt8.nex"
        self.yeastPath = basedir + "/" + self.yeastFile
        self.yeastGenes = self.loadYeast()
        self.geneNum = geneNum
        self.geneList = self.createGeneList(self.geneNum)
        self.sampleOut = "yeast_" + str(self.geneNum) + "_genes.nex"
        self.samplePath = basedir + "/" + self.sampleOut
        self.sampleInfo = "yeast_" + str(self.geneNum) + "_genes_info.nex"
        self.sampleInfoOut = basedir + "/" + self.sampleInfo
        self.concatOut = "yeast_" + str(self.geneNum) + "_concat_genes.nex"
        self.concatPath = basedir + "/" + self.concatOut
        self.nchar = 0
        
    def loadYeast(self):
        ## Imports the yeast gene names into Python into a list
        ## for further use in sampling
        infile = open(self.yeastPath,'r')
        yeastGenes = []
        for line in infile:
            if ("CHARSET" in line):
                temp = line.split()
                yeastGenes.append(temp[1])
        infile.close()
        return yeastGenes
    
    def createGeneList(self, num):
        if (num > len(self.yeastGenes)):
            raise ValueError("Yeast dataset is only " + str(len(self.yeastgenes)) + " members long")
        if (num == 0):
            raise ValueError("Data must have at least one gene")
        ## Note: we don't want to change the original yeast gene list
        ## so we're creating a new list for shuffling here:
        yeastTemp = list(self.yeastGenes)
        ## Set random number seed for reproducibility
        seed(96618)
        shuffle(yeastTemp)
        geneList = yeastTemp[0:num]
        return geneList
        
    def makeSampledNexusFile(self):
        outfile = open(self.samplePath,'w')
        info_outfile = open(self.sampleInfoOut,'w')
        genelinenums = []
        nchar = 0
        for i in range(len(self.geneList)):
            infile = open(self.yeastPath,'r')
            lines = infile.readlines()
           
            ## Find index for the appropriate gene:
            for j in range(len(lines)):
                if (("[" + self.geneList[i] + ",") in lines[j]):
                    genelinenums.append(j)
                    
                if ((self.geneList[i] + " = ") in lines[j]):
                    temp = lines[j].split()
                    temp2 = temp[3].split("-")
                    
                    tempNum = int(temp2[1].rstrip(";")) - int(temp2[0])
                    nchar = nchar + tempNum
                    
            infile.close()
        # Set nchar to preserve it for other functions:
        #nchar = nchar + self.geneNum
        self.nchar = nchar
        
        outfile.write("#NEXUS" + "\n")
        outfile.write("\n")
        outfile.write("Begin data;" + "\n")
        outfile.write("\tDimensions ntax=8 nchar=" + str(nchar + self.geneNum) + ";" + "\n")
        outfile.write("\tFormat datatype=dna missing=? interleave=yes;" + "\n")
        outfile.write("Matrix" + "\n")
        outfile.write("\n")
        infile = open(self.yeastPath,'r')
        lines = infile.readlines()
        for i in range(len(genelinenums)):
            info_outfile.write(self.geneList[i] + "\n")
            outfile.write(lines[genelinenums[i]+1])
            outfile.write(lines[genelinenums[i]+2])
            outfile.write(lines[genelinenums[i]+3])
            outfile.write(lines[genelinenums[i]+4])
            outfile.write(lines[genelinenums[i]+5])
            outfile.write(lines[genelinenums[i]+6])
            outfile.write(lines[genelinenums[i]+7])
            outfile.write(lines[genelinenums[i]+8])
            if not (i == len(genelinenums) -1):
                outfile.write("\n")
        outfile.write(";" + "\n")
        outfile.write("END;" + "\n")
        outfile.close()
        info_outfile.close()
        
    def concatSampNexus(self):
        infile = open(self.samplePath,'r')
        outfile = open(self.concatPath,'w')
        # Prepare lines for taxa
        Scer_line = "Scer "
        Spar_line = "Spar "
        Smik_line = "Smik "
        Skud_line = "Skud "
        Sbay_line = "Sbay "
        Scas_line = "Scas "
        Sklu_line = "Sklu "
        Calb_line = "Calb "
        
        for i in range(7):
                outfile.write(infile.readline())
        for line in infile:
            if ("Scer" in line):
                Scer_line = Scer_line + line.lstrip("Scer ").rstrip("\n")
            if ("Spar" in line):
                Spar_line = Spar_line + line.lstrip("Spar ").rstrip("\n")
            if ("Smik" in line):
                Smik_line = Smik_line + line.lstrip("Smik ").rstrip("\n")
            if ("Skud" in line):
                Skud_line = Skud_line + line.lstrip("Skud ").rstrip("\n")
            if ("Sbay" in line):
                Sbay_line = Sbay_line + line.lstrip("Sbay ").rstrip("\n")
            if ("Scas" in line):
                Scas_line = Scas_line + line.lstrip("Scas ").rstrip("\n")
            if ("Sklu" in line):
                Sklu_line = Sklu_line + line.lstrip("Sklu ").rstrip("\n")
            if ("Calb" in line):
                Calb_line = Calb_line + line.lstrip("Calb ").rstrip("\n")
        
        outfile.write(Scer_line + "\n")
        outfile.write(Spar_line + "\n")
        outfile.write(Smik_line + "\n")
        outfile.write(Skud_line + "\n")
        outfile.write(Sbay_line + "\n")
        outfile.write(Scas_line + "\n")
        outfile.write(Sklu_line + "\n")
        outfile.write(Calb_line + "\n")
        outfile.write(";" + "\n")
        outfile.write("END;" + "\n")
            
                   
            
        