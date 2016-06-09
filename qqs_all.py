'''
Created on Mar 1, 2016

@author: alkpongsema
'''
import shutil
import os
from distribcompare import distribcompare


def treeout(tree, model, treehome):
    if (model == "bayes"):
        treeout = tree + "_bayes_treeout.txt"
    elif (model == "BEAST"):
        #shutil.copyfile(treehome + '/BEAST/' + tree + "treeout.txt", treehome + '/BEAST/' + tree + "BEASTtreeout.txt")
        treeout = tree + "_BEAST_treeout.txt"
    elif (model == "raxml"):
        treeout = tree + "_raxml_treeout.txt"
    elif (model == "phyml"):
        treeout = tree + "_phyml_treeout.txt"
    return treeout

def createQQplots(tree, treehome, model1, model2,xlow,xhigh,ylow,yhigh):
    sturm_version = "SturmMean_130704.jar"
    analysis_jar = "analysis_140702.jar"
    model1out = treeout(tree, model1, treehome)
    model2out = treeout(tree, model2, treehome)
    #shutil.copyfile(treehome + '/' + model1 + '/' + model1out, treehome + '/' + model1out)
    #shutil.copyfile(treehome + '/' + model2 + '/' + model2out, treehome + '/' + model2out)
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
    #treeplot.set_dims(xlow,xhigh,ylow,yhigh)
    #treeplot.qq_plot()

def copyMasterLists(tree, treesteps, models, runNum):
    '''
    Copies and 
    tree = name of the tree
    treesteps = way trees are iterated (i.e. 01, 02, 04, ... or 1, 2, ...
    modeldir = where the list is hiding
    runNum = number of the run you are taking from
    '''
    qqdir = "c:/seqgen/qqstuff"
    basedir = "c:/seqgen"
    for i in range(len(treesteps)):
        for m in range(len(models)):
            treehome = basedir + "/" + tree + treesteps[i] + str(runNum) + "/" + models[m] + "/"
            treeout = tree + treesteps[i] + str(runNum) + "_" + models[m] + "_treeout.txt"
            print("treehome is: " + treehome)
            print("treeout is: " + treeout)
            shutil.copy(treehome + treeout, qqdir + "/" + treeout)
            
def copyAllCoords (tree, treesteps, models, runNum):
    
    qqdir = "c:/seqgen/qqstuff"
    basedir = "c:/seqgen/"
    for i in range(len(treesteps)):
        for m in range(len(models)):
            treehome = basedir + "/" + tree + treesteps[i] + str(runNum) + "/" + models[m] + "/"
            treeout = tree + treesteps[i] + str(runNum) + "_" + models[m] + "_allcoords.txt"
            print("treehome is: " + treehome)
            print("treeout is: " + treeout)
            shutil.copy(treehome + treeout, qqdir + "/" + treeout)


def makeSeparateQQPlots(tree, treesteps, runNum, treehome, models, xhi=.5, yhi=.5):
    '''
    Creates individual QQ plots in png form(without redundancy) for all four models comparing 
    each model to each other.  Plots will be made and placed in the treehome directory.
    tree = name of the tree
    treesteps = tree variant string
    runNum = number of run
    treehome = directory of data for QQ plots
    models = list of models
    '''
    
    for i in range(len(treesteps)):
        tempTree = tree + treesteps[i]+ str(runNum)
        # create plots while avoiding redundancy
        
        for k in range(1,len(models)):
            model1 = models[0]
            model2 = models[k]
            createQQplots(tempTree, treehome, model1, model2, 0, xhi, 0, yhi)
            
        for k in range(2,len(models)):
            model1 = models[1]
            model2 = models[k]
            createQQplots(tempTree, treehome, model1, model2, 0, xhi, 0 ,yhi)
            
        createQQplots(tempTree, treehome, models[2], models[3], 0, xhi, 0,yhi)
        



if __name__ == '__main__':
    
    treeNames = ["leaf","edge","yeast"]
    models = ["bayes","raxml","BEAST","phyml"]
    leafsteps = ["0" + str(n) + 'sameedgesgtr' for n in [1,2,4,6,8]]
    leafsteps.append("10sameedgesgtr")
    edgesteps = ["0" + str(n) + 'CDEgtr' for n in [1,2,4,6,8]]
    edgesteps.append("10CDEgtr")
    yeaststeps = ["_" + str(n) + "_genes" for n in range(1,21)]
    
    treehome = "c:/seqgen/qqstuff"
    runNum = 1
    
    #copyMasterLists("leaf",leafsteps,models,runNum)
    #copyMasterLists("edge",edgesteps,models,runNum)
    #copyMasterLists("yeast",yeaststeps,models,runNum)
    
    #makeSeparateQQPlots(treeNames[0], leafsteps, runNum, treehome, models, .25, .25)
    #makeSeparateQQPlots(treeNames[1], edgesteps, runNum, treehome, models)
    #makeSeparateQQPlots(treeNames[2], yeaststeps, runNum, treehome, models)
    
    leafsteps = ["01sameedgesgtr","10sameedgesgtr"]
    edgesteps = ["01CDEgtr","10CDEgtr"]
    yeaststeps = ["_1_genes","_15_genes","_16_genes","_20_genes"]
    copyAllCoords(treeNames[0], leafsteps, models, runNum)
    copyAllCoords(treeNames[1], edgesteps, models, runNum)
    copyAllCoords(treeNames[2], yeaststeps, models, runNum)