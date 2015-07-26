'''
Created on Jun 26, 2015

@author: alkpongsema
'''

class make_rMDSscript(object):
    '''
    Takes in a distance matrix and makes a 2D or 3D plot using MDS
    '''


    def __init__(self, tree_name, treehome, dist_matrix_file, plot_title, aspect_ratio=0, mean=False, majority=False):
        '''
        Constructor
        '''
        self = self
        self = self
        self.filename = dist_matrix_file 
        self.title = plot_title
        self.treename = tree_name
        self.filepath = treehome
        self.asp = self.asp_test(aspect_ratio)
        self.mean = mean
        self.majority = majority
        self.base_coord1 = 0
        self.base_coord2 = 0
        self.base_color = "cyan"
        self.mean_color = "red1"
        self.majority_color = "goldenrod"
        self.base_pch = "15"
        self.mean_pch = "17"
        self.majority_pch = "19"
        self.png_x = "1000"
        self.png_y = "1000"
        self.suffix = self.set_suffix()
        
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
    
    def set_suffix(self):
        if (self.mean == True and self.majority == True):
            return "_mean_maj_"
        elif (self.mean == True and self.majority == False):
            return "_mean_"
        elif (self.mean == False and self.majority == True):
            return "_majority_"
        else:
            return "_"
        
    def plot_MDS(self,k=2):
        
        outfile = open(self.filepath + self.treename + self.suffix + str(k) + "D.r",'w')
        outfile.write('file_name<- paste("' + self.filepath + self.filename + '",sep="")\n')
        outfile.write('coord_dist<- as.matrix(read.table(file_name))\n')
        outfile.write('dm <- dist(coord_dist, method="euclidean")\n')
        if (k == 2):
            outfile.write('fit <- cmdscale(dm,eig=TRUE,k=' + str(k) + ')\n')
            outfile.write('x <- fit$points[,1]\n')
            outfile.write('y <- fit$points[,2]\n')
        elif (k == 3):
            outfile.write("require(plot3D)\n")
            outfile.write('fit3d <- cmdscale(dm,eig=TRUE,k=' + str(k) + ')\n')
            outfile.write('x <- fit3d$points[,1]\n')
            outfile.write('y <- fit3d$points[,2]\n')
            outfile.write('z <- fit3d$points[,3]\n')
        outfile.write('outfile_png<-paste("' + self.filepath + self.treename + self.suffix +  'MDS_' + str(k) + 'D.png",sep="")\n')
        outfile.write('outfile_pdf<-paste("' + self.filepath + self.treename + self.suffix + 'MDS_' + str(k) + 'D.pdf",sep="")\n')
        outfile.write('plotcolors<-rep("black",1002) '+"\n")
        outfile.write('plotpch<-rep(1,1002) '+"\n")
        outfile.write('plotcolors[1] = "' + self.base_color + '" \n')
        outfile.write('plotpch[1] = ' + self.base_pch + ' \n')
        
        if (self.mean == True and self.majority == True):
            outfile.write('plotcolors[2] ="' + self.mean_color+'" \n')
            outfile.write('plotcolors[3] ="' + self.majority_color+'"\n')
            outfile.write('plotpch[2] = ' + self.mean_pch+' \n')
            outfile.write('plotpch[3] = ' + self.majority_pch+' \n')
        
        elif (self.mean == True and self.majority == False):
            outfile.write('plotcolors[2] ="' + self.mean_color+'" \n')
            outfile.write('plotpch[2] = ' + self.mean_pch+' \n')

        elif (self.mean == False and self.majority == True):
            outfile.write('plotcolors[2] ="' + self.majority_color+'" \n')
            outfile.write('plotpch[2] = ' + self.majority_pch+' \n')
        elif (self.mean == False and self.majority == False):
            pass
        #PDF section:
        
        outfile.write('pdf(outfile_pdf)\n')
        if (k == 2):
            outfile.write('plot(x,y,col=c(plotcolors),pch=c(plotpch),main="'+ self.title + self.asp+')\n')
        elif (k == 3):
            outfile.write('scatter3D(x,y,z,col=c(plotcolors),pch=c(plotpch),main="'+ self.title + self.asp+')\n')
        outfile.write('dev.off()\n')   
        
        #PNG section:
        
        outfile.write('png(outfile_png,width=' + self.png_x + ",height=" +  self.png_y + ')\n')
        if (k == 2):
            outfile.write('plot(x,y,col=c(plotcolors),pch=c(plotpch),main="'+ self.title + self.asp+')\n')
        elif (k == 3):
            outfile.write('scatter3D(x,y,z,col=c(plotcolors),pch=c(plotpch),main="'+ self.title + self.asp+')\n')
        outfile.write('dev.off()\n')
        
        outfile.close()