    file_name<- paste("C:/PyStuff/BioScripting/test/coords/coords.txt",sep="")
    data1<-read.table(file_name,col.names=c("coord1","coord2","coord3","coord4","coord5","coord6","coord7"))
    file_name<- paste("C:/PyStuff/BioScripting/test/coords/coords_2.txt",sep="")
    data2<-read.table(file_name,col.names=c("coord1","coord2","coord3","coord4","coord5","coord6","coord7"))
    file_name<- paste("C:/PyStuff/BioScripting/test/coords/coords_3.txt",sep="")
    data3<-read.table(file_name,col.names=c("coord1","coord2","coord3","coord4","coord5","coord6","coord7"))
    file_name<- paste("C:/PyStuff/BioScripting/test/coords/coords_4.txt",sep="")
    data4<-read.table(file_name,col.names=c("coord1","coord2","coord3","coord4","coord5","coord6","coord7"))
    plot_title<-paste("Logmap of Topologies",sep=" ")
    outfile_name<-paste("C:/PyStuff/BioScripting/test/quadrant_plots/all_topo_logmap.png",sep="")
    outfile_pdf<-paste("C:/PyStuff/BioScripting/test/quadrant_plots/all_topo_logmap.pdf",sep="")
    
    pdf(outfile_pdf)
    plot.default(data1$coord1,data1$coord2,xlim=c(-20,50),ylim=c(-5,50),xlab="coord1",ylab="coord2",main=plot_title)
    points(1,10,col=69,pch=15)
    dev.off()
    
    png(outfile_name,width=400,height=400)
    plot.default(data1$coord1,data1$coord2,xlim=c(-20,50),ylim=c(-5,50),xlab="coord1",ylab="coord2",main=plot_title)
    points(1,10,col=69,pch=15)
    dev.off()