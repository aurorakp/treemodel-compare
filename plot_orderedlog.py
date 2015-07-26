'''
Created on Jul 16, 2015

@author: alkpongsema
'''
from subprocess import call

class plot_orderedlog(object):
    '''
    classdocs
    '''


    def __init__(self, treename, treehome, model):
        '''
        Constructor
        '''
        self.treename = treename
        self.treehome = treehome
        self.model = model
        self.out = treehome + '/' + model + '/quadrant_plots/' + treename + '_' + model + '_' + "logplots.R"
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
        
        # All quadrants relative to centre #1:
        outfile.write('file_name<- paste("' + self.treehome + "/" + self.model + "/"   + self.treename + '_'+ self.model +'_ordered_allcoords.txt",sep="")\n')
        outfile.write('data<-read.table(file_name)\n')
        outfile.write('names(data) <-c("coord1","coord2")\n')
        outfile.write('plot_title<-paste("Ordered Coordinates Relative to Topology #1 Centre",sep=" ")\n')
        outfile.write('plotcolors.palette <- colorRampPalette(c("blue","red"),space="Lab")\n')
        outfile.write('outfile_name<-paste("' + self.treehome + "/" + self.model + '/quadrant_plots/' + self.treename + '_ordered_all_topos.pdf",sep="")\n')
        outfile.write('pdf(outfile_name)\n')
        outfile.write('plot.default(data$coord1,data$coord2,col = plotcolors.palette(1003), main=plot_title,asp=1)\n')
        outfile.write('dev.off()\n')
        outfile.write('file_name<- paste("' + self.treehome + "/" + self.model + "/"   + self.treename + '_'+ self.model +'_ordered_allcoords.txt",sep="")\n')
        outfile.write('data<-read.table(file_name)\n')
        outfile.write('names(data) <-c("coord1","coord2")\n')
        outfile.write('plot_title<-paste("Ordered Coordinates Relative to Topology #1 Centre",sep=" ")\n')
        outfile.write('plotcolors.palette<-colorRampPalette(c("red","blue"),space="rgb")'+"\n")
        outfile.write('outfile_png<-paste("' + self.treehome + "/" + self.model + '/quadrant_plots/' + self.treename + 'ordered_all_topos.png",sep="")\n')
        outfile.write('png(outfile_png,width=' + self.pngwidth + ',height=' + self.pngheight + ')\n')
        outfile.write('plot.default(data$coord1,data$coord2,col = plotcolors.palette(1003), main=plot_title,asp=1)\n')
        outfile.write('dev.off()')    
        outfile.close()
        
    def makePlots(self):
        command = 'C:/Rstuff/R-3.2.0/bin/Rscript.exe ' + self.out 
        call(command.split())