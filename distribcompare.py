'''
Created on Jun 24, 2015

@author: alkpongsema
'''

import re
import os
import subprocess


class distribcompare(object):
    '''
    Takes two tree files, finds their mean tree, and uses a QQ plot to compare the tree distributions
    '''


    def __init__(self, plotname, treefile1, treefile2, qq_dir, t1rooted=False, t2rooted=False, mean_jar = "SturmMean_130704.jar", analysis_jar = "analysis_140702.jar"):
        '''
        Constructor
        Condition: treefile1 and treefile2 must be two distinct files
        '''
        self = self
        self.plotname = plotname
        self.tree_file_1 = treefile1
        self.tree_file_2 = treefile2
        self.tree_mean_1 = re.sub(r'([.].+)',"",treefile1) + "_mean.txt"
        self.tree_mean_2 = re.sub(r'([.].+)',"",treefile2) + "_mean.txt"
        self.dist_to_mean_1 = re.sub(r'([.].+)',"",treefile1) + "_dist.txt"
        self.dist_to_mean_2 = re.sub(r'([.].+)',"",treefile2) + "_dist.txt"
        if (treefile1 == treefile2):
            raise Exception("Must input tree files with different names.")
        self.sturm_version = mean_jar
        self.analysis_version = analysis_jar
        self.qqdir = qq_dir
        self.qqfileout = qq_dir + "/" + plotname
        self.t1rooted = self.rooted_flag(t1rooted)
        self.t2rooted = self.rooted_flag(t2rooted)
        self.xlow = 0.0
        self.xhigh = 1.0
        self.ylow = 0.0
        self.yhigh = 1.0
        
    def rooted_flag(self, rooted):
        if (rooted == False):
            return " -u"
        else:
            return ""
        
    def set_dims(self, xlow, xhigh, ylow, yhigh):
        self.xlow = xlow
        self.xhigh = xhigh
        self.ylow = ylow
        self.yhigh = yhigh
    
    def find_means(self):
        os.chdir(self.qqdir)
        if not os.path.exists(self.tree_mean_1):
            command = "java -jar " + self.sturm_version + self.t1rooted + " -a random -e 0.0001 -o " + self.tree_mean_1 + " " + self.tree_file_1
            subprocess.call(command.split())
        else:
            print "Skipping mean creation for tree 1 - already done"
        if not os.path.exists(self.tree_mean_2):
            command = "java -jar " + self.sturm_version + self.t2rooted + " -a random -e 0.0001 -o " + self.tree_mean_2 + " " + self.tree_file_2
            subprocess.call(command.split())
        else:
            print "Skipping mean creation for tree 2 - already done"
            
    def find_disttomean(self):
        os.chdir(self.qqdir)
        if not os.path.exists(self.dist_to_mean_1):
            command = 'java -jar ' + self.analysis_version + self.t1rooted + ' -a gtp_twofiles -o ' + self.dist_to_mean_1 + ' -f '  + self.tree_file_1 + " " + self.tree_mean_1
            subprocess.call(command.split())
        else:
            print "Skipping distances to mean for tree 1 - already done"
        if not os.path.exists(self.dist_to_mean_2):
            command = 'java -jar ' + self.analysis_version + self.t2rooted + ' -a gtp_twofiles -o ' + self.dist_to_mean_2 + ' -f '  + self.tree_file_2 + " " + self.tree_mean_2
            subprocess.call(command.split())
        else:
            print "Skipping distances to mean for tree 2 - already done"
    def qq_plot(self):
        os.chdir(self.qqdir)
        if not os.path.exists(self.qqfileout + ".r"):
            qq_out = open(self.qqfileout + ".r",'w')
            qq_out.write('filename1 <- paste ("' + self.dist_to_mean_1 + '",sep="")' + "\n")
            qq_out.write('filename2 <- paste ("' + self.dist_to_mean_2 + '",sep="")' + "\n")
            qq_out.write('data1 <- read.table(filename1, col.names=c("index1","index2","dist"))' + "\n")
            qq_out.write('data2 <- read.table(filename2, col.names=c("index1","index2","dist"))' + "\n")
            qq_out.write('plot_title <- paste("QQ Plot for ' +  re.sub(r'([.].+)',"",self.tree_file_1) +  " and " + re.sub(r'([.].+)',"",self.tree_file_2) +  '",sep="")' + "\n")
            qq_out.write('xlabel <- paste("Distance to Mean Tree for ' + re.sub(r'([.].+)',"",self.tree_file_1)+ '",sep="")' + "\n")
            qq_out.write('ylabel <- paste("Distance to Mean Tree for ' + re.sub(r'([.].+)',"",self.tree_file_2)+ '",sep="")' + "\n")
            qq_out.write('outfile_pdf <- paste("' + self.qqfileout + '.pdf",sep="")' + "\n")
            qq_out.write('outfile_png <- paste("' + self.qqfileout + '.png",sep="")' + "\n")
            qq_out.write('pdf(outfile_pdf)' + "\n")
            qq_out.write('qqplot(data1$dist, data2$dist, plot.it = TRUE, main = plot_title, xlim = c(' + str(self.xlow) + ',' + str(self.xhigh) + '), ylim = c(' + str(self.ylow) + ',' + str(self.yhigh) + '), xlab = xlabel, ylab = ylabel, asp=1)' + "\n")
            qq_out.write('abline(a=0,b=1,untf=FALSE)' + "\n")
            qq_out.write('dev.off()' + "\n")
            qq_out.write('png(outfile_png,width=1000,height=1000)' + "\n")
            qq_out.write('qqplot(data1$dist, data2$dist, plot.it = TRUE, main = plot_title, xlim = c(' + str(self.xlow) + ',' + str(self.xhigh) + '), ylim = c(' + str(self.ylow) + ',' + str(self.yhigh) + '), ylab = ylabel,asp=1)' + "\n")
            qq_out.write('abline(a=0,b=1,untf=FALSE)' + "\n")
            qq_out.write('dev.off()')
            qq_out.close()
        else:
            print "Skipping R script generation - already done"
        if not os.path.exists(self.qqfileout + ".pdf" or self.qqfileout + ".png"):
            command = 'rscript ' + self.qqfileout + ".r"
            subprocess.call(command.split())
        else:
            print "Skipping QQ Plot generation - already done"
            
        
        
        
        
        
        