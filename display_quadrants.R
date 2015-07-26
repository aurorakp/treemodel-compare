# Print out the sampled means

for(n in 1:3) {
	file_name<-paste("C:/PyStuff/BioScripting/test/coords/coords_",n,".txt",sep="")
	data<-read.table(file_name,col.names=c("edge1","edge2","leaf1","leaf2","leaf3","leaf4"))

	plot_title<-paste("Topology",n,sep =" ")
	outfile_name<-paste("C:/PyStuff/BioScripting/test/split_by_topology/topo_",n,".pdf",sep="")
	pdf(outfile_name)
	plot.default(data$edge1,data$edge2,main=plot_title,asp=1)
	dev.off()
	
	# plot the histogram of the coordinate corresponding to edge p
    hist_name<-paste("C:/PyStuff/BioScripting/test/quadrant_plots/hist_topo_",n,".pdf",sep="")
    pdf(hist_name)
	hist(data$edge1)
	dev.off()
	
	# plot the histogram of just the coordinates "on" (up to error) the p axis
	
	# if (n ==1){
		# hist_name<-"C:/PyStuff/BioScripting/test/quadrant_plots/hist_topo_1_axis.pdf"
    	# pdf(hist_name)
    	# axis_data<-data[which(data$edge1 <0.0001),]
    	# hist(axis_data$edge2,main="Histogram of p axis value of sample means within 0.0001 of p axis")
		# dev.off()
	# }
	
}
