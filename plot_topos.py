'''
Created on Jul 14, 2015

@author: alkpongsema
'''

from subprocess import call

class plot_topos(object):
    '''
    This creates logmap quadrant plots relative 
    '''


    def __init__(self, treename, treehome, model, topNum=1):
        '''
        treehome should be the tree + model version
        
        '''
        self.treename = treename
        self.treehome = treehome
        self.model = model
        self.out = treehome + 'quadrant_plots/' + treename + '_' + model + '_' + "logplots.R"
        self.topNum = topNum
        self.pngwidth = "1000"
        self.pngheight = "1000"
        
    def set_png_width(self, width=1000):
        self.pngwidth = str(width)
    def set_png_height(self, height=1000):
        self.pngheight = str(height)
    def set_png_dim(self, width=1000, height=1000):
        self.set_png_width(width)
        self.set_png_height(height)
    
    def makeScript(self):
        outfile = open(self.out,'w')
        # Quadrants
        outfile.write("for (n in 1:" + str(self.topNum) + ") {\n")
        outfile.write('file_name<- paste("' + self.treehome + '/coords/coords_",n,".txt",sep="")\n')
        outfile.write('data<-read.table(file_name)\n')
        outfile.write('names(data) <-c("coord1","coord2")\n')
        outfile.write('plot_title<-paste("Topology",n,sep=" ")\n')
        outfile.write('plotcolors.palette <- colorRampPalette(c("blue","red"),space="Lab")\n')
        outfile.write('outfile_name<-paste("' + self.treehome + '/quadrant_plots/topo_",n,".pdf",sep="")\n')
        outfile.write('pdf(outfile_name)\n')
        outfile.write('plot.default(data$coord1,data$coord2,col = plotcolors.palette(1003),main=plot_title,asp=1)\n')
        outfile.write('dev.off()\n')
        outfile.write('}\n')
        outfile.write("for (n in 1:" + str(self.topNum) + ") {\n")
        outfile.write('file_name<- paste("' + self.treehome + '/coords/coords_",n,".txt",sep="")\n')
        outfile.write('data<-read.table(file_name)\n')
        outfile.write('names(data) <-c("coord1","coord2")\n')
        outfile.write('plot_title<-paste("Topology",n,sep=" ")\n')
        outfile.write('plotcolors.palette <- colorRampPalette(c("blue","red"),space="Lab")\n')
        outfile.write('outfile_png<-paste("' + self.treehome + '/quadrant_plots/topo_",n,".png",sep="")\n')
        outfile.write('png(outfile_png,width=' + self.pngwidth + ',height=' + self.pngheight + ')\n')
        outfile.write('plot.default(data$coord1,data$coord2,col = plotcolors.palette(1003), main=plot_title,asp=1)\n')
        outfile.write('}\n')
        outfile.write('dev.off()\n')
        # All quadrants relative to centre #1:
        outfile.write('file_name<- paste("' + self.treehome + self.treename + self.model + '_allcoords.txt",sep="")\n')
        outfile.write('data<-read.table(file_name)\n')
        outfile.write('names(data) <-c("coord1","coord2")\n')
        # Order the data coording to coordinate #2:
        outfile.write('plot_title<-paste("Coordinates Relative to Topology #1 Centre",sep=" ")\n')
        outfile.write('plotcolors.palette <- colorRampPalette(c("blue","red"),space="Lab")\n')
        outfile.write('outfile_name<-paste("' + self.treehome + '/quadrant_plots/' + self.treename + '_all_topos.pdf",sep="")\n')
        outfile.write('pdf(outfile_name)\n')
        outfile.write('plot.default(data$coord1,data$coord2,col = plotcolors.palette(1003), main=plot_title,asp=1)\n')
        outfile.write('dev.off()\n')
        outfile.write('file_name<- paste("' + self.treehome + self.treename + self.model + '_allcoords.txt",sep="")\n')
        outfile.write('data<-read.table(file_name)\n')
        outfile.write('names(data) <-c("coord1","coord2")\n')
        outfile.write('plot_title<-paste("Coordinates Relative to Topology #1 Centre",sep=" ")\n')
        outfile.write('plotcolors<-colorRampPalette(c("red","blue"),space="rgb")'+"\n")
        outfile.write('outfile_png<-paste("' + self.treehome + '/quadrant_plots/' + self.treename + '_all_topos.png",sep="")\n')
        outfile.write('png(outfile_png,width=' + self.pngwidth + ',height=' + self.pngheight + ')\n')
        outfile.write('plot.default(data$coord1,data$coord2,col = plotcolors.palette(1003), main=plot_title,asp=1)\n')
        outfile.write('dev.off()')    
        outfile.close()
    
    def makePlots(self):
        command = 'C:/Rstuff/R-3.2.0/bin/Rscript.exe ' + self.out 
        call(command.split())
