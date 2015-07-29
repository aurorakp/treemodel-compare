filename1 = <- paste ( self.dist_to_mean_1,sep="")
filename2 = <- paste ( self.dist_to_mean_2,sep="")
data1 <- read.table(filename1, col.names=c("index1","index2","dist"))
data2 <- read.table(filename2, col.names=c("index1","index2","dist"))
plot_title <- paste("QQ Plot for" treefile1 " and" treefile2 ":",sep="")
outfile_pdf <- paste(self.qqfileout ".pdf",sep="")
outfile_png <- paste(self.qqfileout ".png",sep="")
pdf(outfile_pdf)
qqplot(data1$dist, data2$dist, plot.it = TRUE, main = plot_title)
dev.off()
png(outfile_png,width=1000,height=1000)
qqplot(data1$dist, data2$dist, plot.it = TRUE, main = plot_title)
dev.off()