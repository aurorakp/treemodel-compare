
'''
Created on Jun 18, 2015

@author: alkpongsema
'''
import os

class make_rplotscript(object):
    '''
    Automates an R script designed to plot tree distributions on a Euclidean plane given an x,y coordinate conversion
    using logmap or MDS.
    '''


    def __init__(self, file_dir, file_name, plot_title, aspect_ratio=0, outdir = "", normfile = "", mean=False, majority=False):
        '''
        Constructor
        '''
        self = self
        self.filename = file_dir + file_name 
        self.title = plot_title
        self.filepath = file_dir + "/" + file_name[0:-4]
        self.outdir = outdir
        self.outpath = outdir + "/" + file_name[0:-4]
        self.outfile = self.filename[0:-4] + '.r'
        self.normoutfile = self.filename[0:-4] + "_norm3D.r"
        self.normoutpath = outdir + "/" + file_name[0:-4] + "_norm3D"
        self.asp = self.asp_test(aspect_ratio)
        self.mean = mean
        self.majority = majority
        self.base_coord1 = 0
        self.base_coord2 = 0
        self.base_color = "69"
        self.mean_color = "chartreuse"
        self.majority_color = "darkorchid1"
        self.base_pch = "15"
        self.mean_pch = "17"
        self.majority_pch = "19"
        self.png_x = "1000"
        self.png_y = "1000"
        self.normfile = normfile
        
    def setNormFile(self,normfile=""):
        self.normfile = normfile
        
    def setOutdir(self,outdir=""):
        self.outdir = outdir
        
    def asp_test(self, aspect_ratio):
        if (aspect_ratio == 0):
            return '"'
        else:
            return '",asp=' + str(aspect_ratio) 
        
    def set_base(self, coord1, coord2):
        self.base_coord1 = coord1
        self.base_coord2 = coord2
    
    def set_colors(self, base, mean, majority):
        self.base_color = ",col=" + str(base)
        self.mean_color = ",col=" + str(mean)
        self.majority_color = ",col=" + str(majority)
    
    def set_pch(self, base, mean, majority):
        self.base_pch = ",pch=" + str(base)
        self.mean_pch = ",pch=" + str(mean)
        self.majority_pch = ",pch=" + str(majority)
    
    def set_png_dim(self, width, height):
        self.png_x = str(width)
        self.png_y = str(height)
        
    def rplot(self, base=False):
        # Plots the graph while allowing us to specify the 'base tree coordinates' first.
        # Requires use of set_base first if a base tree is desired
        
        # PDF section:
        
        r_file = open(self.outfile,'w') 
        r_file.write('file_name<- paste("' + self.filename +'",sep="")'+"\n")
        r_file.write('data<-read.table("' + self.filename + '",)'+"\n")
        r_file.write('names(data) <- c("coord1","coord2")'+"\n")
        r_file.write('plot_title<-paste("' + self.title +'",sep="")'+"\n")
       
        r_file.write('outfile_pdf<-paste("'+ self.outpath + '.pdf",sep="")'+"\n")
        r_file.write('pdf(outfile_pdf)\n')
        
       
        if (self.mean == False and self.majority == False):
            r_file.write('plot.default(data$coord1,data$coord2,main="' + self.title + self.asp+')\n')
        
        elif (self.mean == True and self.majority == True):
            # This assumes the mean tree is on line 1 and majority is on line 2:
            r_file.write('plotcolors<-rep("black",1002)'+"\n")
            r_file.write('plotcolors[1] ="' + self.mean_color+'"\n')
            r_file.write('plotcolors[2] ="' + self.majority_color+'"\n')
            r_file.write('plotpch<-rep(1,1002)'+"\n")
            r_file.write('plotpch[1] =' + self.mean_pch+'\n')
            r_file.write('plotpch[2] =' + self.majority_pch+'\n')
            r_file.write('plot.default(data$coord1,data$coord2,col=plotcolors,pch=plotpch,main="'+ self.title + self.asp+')\n')
            
            
        elif (self.mean == True and self.majority == False):
            r_file.write('plotcolors<-rep("black",1002)'+"\n")
            r_file.write('plotcolors[1] ="' + self.mean_color+'"\n')
            r_file.write('plotpch<-rep(1,1002)'+"\n")
            r_file.write('plotpch[1] =' + self.mean_pch+'\n')
            r_file.write('plot.default(data$coord1,data$coord2,col=plotcolors,pch=plotpch,main="'+ self.title + self.asp+')\n')
           
            
        elif (self.mean == False and self.majority == True):
            r_file.write('plotcolors<-rep("black",1002)'+"\n")
            r_file.write('plotcolors[1] ="' + self.majority_color+'"\n')
            r_file.write('plotpch<-rep(1,1002)'+"\n")
            r_file.write('plotpch[1] =' + self.majority_pch+'\n')
            r_file.write('plot.default(data$coord1,data$coord2,col=plotcolors,pch=plotpch,main="'+ self.title + self.asp+')\n')
            
            
        if (base==True):
            r_file.write("points(" + str(self.base_coord1) + "," + str(self.base_coord2) + ", " + "col=" + self.base_color + ",pch=" + self.base_pch + ")"+"\n")
            
        r_file.write("dev.off()"+"\n")
        
        # PNG section:
                
        r_file.write('outfile_png<-paste("' + self.outpath + '.png",sep="")'+"\n")
        r_file.write('png(outfile_png,width=' + self.png_x + ',height=' + self.png_y+')\n')
        

        if (self.mean == False and self.majority == False):
            r_file.write('plot.default(data$coord1,data$coord2,main="' + self.title + self.asp+')\n')
   
        elif (self.mean == True and self.majority == True):
            # This assumes the mean tree is on line 1 and majority is on line 2:
            r_file.write('plotcolors<-rep("black",1002)'+"\n")
            r_file.write('plotcolors[1] ="' + self.mean_color+'"\n')
            r_file.write('plotcolors[2] ="' + self.majority_color+'"\n')
            r_file.write('plotpch<-rep(1,1002)'+"\n")
            r_file.write('plotpch[1] =' + self.mean_pch+"\n")
            r_file.write('plotpch[2] =' + self.majority_pch+"\n")
            r_file.write('plot.default(data$coord1,data$coord2,col=plotcolors,pch=plotpch,main="'+ self.title + self.asp+')\n')
            
            
        elif (self.mean == True and self.majority == False):
            r_file.write('plotcolors<-rep("black",1002)'+"\n")
            r_file.write('plotcolors[1] ="' + self.mean_color+'"\n')
            r_file.write('plotpch<-rep(1,1002)'+"\n")
            r_file.write('plotpch[1] =' + self.mean_pch+'\n')
            r_file.write('plot.default(data$coord1,data$coord2,col=plotcolors,pch=plotpch,main="'+ self.title + self.asp+')\n')
            
                
        elif (self.mean == False and self.majority == True):
            r_file.write('plotcolors<-rep("black",1002)'+"\n")
            r_file.write('plotcolors[1] ="' + self.majority_color+'"\n')
            r_file.write('plotpch<-rep(1,1002)'+"\n")
            r_file.write('plotpch[1] =' + self.majority_pch+'\n')
            r_file.write('plot.default(data$coord1,data$coord2,col=plotcolors,pch=plotpch,main="'+ self.title + self.asp+')\n')
            
            
        if (base==True):
            r_file.write("points(" + str(self.base_coord1) + "," + str(self.base_coord2) + ", " + "col=" + self.base_color + ",pch=" + self.base_pch + ")"+"\n")
        
        r_file.write("dev.off()"+"\n")
        
        r_file.close()  
        
    def rplotnorm(self,base=False):
        # Plots the graph while allowing us to specify the 'base tree coordinates' first.
        # Requires use of set_base first if a base tree is desired
        
        # PDF section:
        
        r_file = open(self.normoutfile,'w') 
        r_file.write('file_name<- paste("' + self.filename +'",sep="")'+"\n")
        r_file.write('file_norm<- paste("' + self.normfile +'",sep="")'+"\n")
        r_file.write('data1<-read.table(' + "file_name" + ')'+"\n")
        r_file.write('data2<-read.table(' + "file_norm" + ')'+"\n")
        r_file.write('names(data1) <- c("coord1","coord2")'+"\n")
        r_file.write('data <- data.frame(data1$coord1,data1$coord2,data2)' + "\n")
        r_file.write('names(data) <-c("coord1","coord2","norm")'+"\n")
        r_file.write('plot_title<-paste("' + self.title +'",sep="")'+"\n")
       
        r_file.write('outfile_pdf<-paste("'+ self.normoutpath + '.pdf",sep="")'+"\n")
        r_file.write('pdf(outfile_pdf)\n')
        r_file.write("require(plot3D)\n")
       
        if (self.mean == False and self.majority == False):
      
            r_file.write('scatter3D(data$coord1,data$coord2,data$norm,main="'+ self.title + self.asp+')\n')

        
        elif (self.mean == True and self.majority == True):
            # This assumes the mean tree is on line 1 and majority is on line 2:
            r_file.write('plotcolors<-rep("black",1002)'+"\n")
            r_file.write('plotcolors[1] ="' + self.mean_color+'"\n')
            r_file.write('plotcolors[2] ="' + self.majority_color+'"\n')
            r_file.write('plotpch<-rep(1,1002)'+"\n")
            r_file.write('plotpch[1] =' + self.mean_pch+'\n')
            r_file.write('plotpch[2] =' + self.majority_pch+'\n')
            r_file.write('scatter3D(data$coord1,data$coord2,data$norm,col=plotcolors,pch=plotpch,main="'+ self.title + self.asp+')\n')

            
            
        elif (self.mean == True and self.majority == False):
            r_file.write('plotcolors<-rep("black",1002)'+"\n")
            r_file.write('plotcolors[1] ="' + self.mean_color+'"\n')
            r_file.write('plotpch<-rep(1,1002)'+"\n")
            r_file.write('plotpch[1] =' + self.mean_pch+'\n')
            r_file.write('scatter3D(data$coord1,data$coord2,data$norm,col=plotcolors,pch=plotpch,main="'+ self.title + self.asp+')\n')
           
            
        elif (self.mean == False and self.majority == True):
            r_file.write('plotcolors<-rep("black",1002)'+"\n")
            r_file.write('plotcolors[1] ="' + self.majority_color+'"\n')
            r_file.write('plotpch<-rep(1,1002)'+"\n")
            r_file.write('plotpch[1] =' + self.majority_pch+'\n')
            r_file.write('scatter3D(data$coord1,data$coord2,data$norm,col=plotcolors,pch=plotpch,main="'+ self.title + self.asp+')\n')
            
            
        if (base==True):
            r_file.write("points(" + str(self.base_coord1) + "," + str(self.base_coord2) + ", " + "col=" + self.base_color + ",pch=" + self.base_pch + ")"+"\n")
            
        r_file.write("dev.off()"+"\n")
        
        # PNG section:
                
        r_file.write('outfile_png<-paste("' + self.normoutpath + '.png",sep="")'+"\n")
        r_file.write('png(outfile_png,width=' + self.png_x + ',height=' + self.png_y+')\n')
        r_file.write("require(plot3D)\n")

        if (self.mean == False and self.majority == False):
            r_file.write('scatter3D(data$coord1,data$coord2,data$norm,main="'+ self.title + self.asp+')\n')
        elif (self.mean == True and self.majority == True):
            # This assumes the mean tree is on line 1 and majority is on line 2:
            r_file.write('plotcolors<-rep("black",1002)'+"\n")
            r_file.write('plotcolors[1] ="' + self.mean_color+'"\n')
            r_file.write('plotcolors[2] ="' + self.majority_color+'"\n')
            r_file.write('plotpch<-rep(1,1002)'+"\n")
            r_file.write('plotpch[1] =' + self.mean_pch+'\n')
            r_file.write('plotpch[2] =' + self.majority_pch+'\n')
            r_file.write('scatter3D(data$coord1,data$coord2,data$norm,col=plotcolors,pch=plotpch,main="'+ self.title + self.asp+')\n')
            
            
        elif (self.mean == True and self.majority == False):
            r_file.write('plotcolors<-rep("black",1002)'+"\n")
            r_file.write('plotcolors[1] ="' + self.mean_color+'"\n')
            r_file.write('plotpch<-rep(1,1002)'+"\n")
            r_file.write('plotpch[1] =' + self.mean_pch+'\n')
            r_file.write('scatter3D(data$coord1,data$coord2,data$norm,col=plotcolors,pch=plotpch,main="'+ self.title + self.asp+')\n')
            
                
        elif (self.mean == False and self.majority == True):
            r_file.write('plotcolors<-rep("black",1002)'+"\n")
            r_file.write('plotcolors[1] ="' + self.majority_color+'"\n')
            r_file.write('plotpch<-rep(1,1002)'+"\n")
            r_file.write('plotpch[1] =' + self.majority_pch+'\n')
            r_file.write('scatter3D(data$coord1,data$coord2,data$norm,col=plotcolors,pch=plotpch,main="'+ self.title + self.asp+')\n')
            
            
        if (base==True):
            r_file.write("points(" + str(self.base_coord1) + "," + str(self.base_coord2) + ", " + "col=" + self.base_color + ",pch=" + self.base_pch + ")"+"\n")
        
        r_file.write("dev.off()"+"\n")
        
        r_file.close()  
            
            
    
    