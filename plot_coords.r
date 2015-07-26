for (n in 1:15) {
    file_name<- paste("C:/PyStuff/BioScripting/test/coords/coords_",n,".txt",sep="")
    data<-read.table(file_name,col.names=c("coord1","coord2","coord3","coord4","coord5","coord6","coord7"))
    plot_title<-paste("Topology",n,sep=" ")
    outfile_name<-paste("C:/PyStuff/BioScripting/test/quadrant_plots/topo_",n,".pdf",sep="")
    pdf(outfile_name)
    plot.default(data$coord1,data$coord2,man=plot_title,asp=1)
    points(1,10,col=69,pch=15)
    dev.off()
    }
for (n in 1:15) {
    file_name<- paste("C:/PyStuff/BioScripting/test/coords/coords_",n,".txt",sep="")
    data<-read.table(file_name,col.names=c("coord1","coord2","coord3","coord4","coord5","coord6","coord7"))
    plot_title<-paste("Topology",n,sep=" ")
    outfile_png<-paste("C:/PyStuff/BioScripting/test/quadrant_plots/topo_",n,".png",sep="")
    png(outfile_png,width=240,height=240)
    plot.default(data$coord1,data$coord2,man=plot_title,asp=1)
    points(1,10,col=69,pch=15)
    dev.off()	
   }