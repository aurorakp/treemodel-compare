file_name<- paste("C:/PyStuff/BioScripting/test/basenew_allcoords.txt",sep="")
coord_dist <- as.matrix(read.table(file_name))
dm <- dist(coord_dist, method="euclidean")
fit <- cmdscale(dm,eig=TRUE,k=2)
x <- fit$points[,1]
y <- fit$points[,2]

outfile_png<-paste("C:/PyStuff/BioScripting/test/quadrant_plots/MDS_alltopo.png",sep="")
outfile_pdf<-paste("C:/PyStuff/BioScripting/test/quadrant_plots/MDS_alltopo.pdf",sep="")
pdf(outfile_pdf)
plot(x,y,main="Topologies under MDS",asp=1)
points(1,10,col=69,pch=15)

dev.off()   

png(outfile_png,width=240,height=240)
plot(x,y,main="Topologies under MDS",asp=1)
points(1,10,col=69,pch=15)
dev.off()

for (n in 1:2) {
    file_name<- paste("C:/PyStuff/BioScripting/test/coords/coords_",n,".txt",sep="")
    coord_dist <- as.matrix(read.table(file_name))
    dm <- dist(coord_dist, method="euclidean")
    fit <- cmdscale(dm,eig=TRUE,k=2)
    x <- fit$points[,1]
    y <- fit$points[,2]
    plot_title<-paste("Topology",n,sep=" ")
    outfile_name<-paste("C:/PyStuff/BioScripting/test/quadrant_plots/topoMDS_",n,".pdf",sep="")
    plot_title = paste("Topology",n,"under MDS",sep="")
    pdf(outfile_name)
    plot(x,y,main=plot_title,asp=1)
    points(1,10,col=69,pch=15)
    dev.off()
    }
for (n in 1:2) {
    file_name<- paste("C:/PyStuff/BioScripting/test/coords/coords_",n,".txt",sep="")
    coord_dist <- as.matrix(read.table(file_name))
    dm <- dist(coord_dist, method="euclidean")
    fit <- cmdscale(dm,eig=TRUE,k=2)
    x <- fit$points[,1]
    y <- fit$points[,2]
    plot_title<-paste("Topology",n,"under MDS",sep="")
    outfile_png<-paste("C:/PyStuff/BioScripting/test/quadrant_plots/topoMDS_",n,".png",sep="")
    png(outfile_png,width=800,height=800)
    plot(x,y,main=plot_title,asp=1)
    points(1,10,col=69,pch=15)
    dev.off()	
   }