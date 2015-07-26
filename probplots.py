'''
Created on Jun 24, 2015

@author: alkpongsema
'''
from distribcompare import distribcompare

if __name__ == '__main__':
    #treeplot = distribcompare("newbasetreeout.txt", "basenewtreeout.txt")
    #treeplot = distribcompare("basenew_raxmlout.txt","newbase_raxmlout.txt")
    #treeplot = distribcompare("newbasetreeout.txt","newbase_raxmlout.txt")
    treeplot = distribcompare("basenewtreeout.txt","basenew_raxmlout.txt")
    treeplot.find_means()
    treeplot.find_disttomean()
    treeplot.qq_plot()  