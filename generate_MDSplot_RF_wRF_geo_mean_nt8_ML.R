# All trees from the nt8_ML file of Rokas et al.

# Create both a 2D and 3D MDS plot of these trees.

# Distances between are RF and weighted RF.


library("rgl")

# Read in dissimilarity matrix
data_RF<-scan("/Users/megan/research/projects/validating_mean_var_out_of_sync_with_office/experiments/2012-10-07_MDS_Rokas_with_mean/diss_RF_mean_nt8_ML")
dist_mat_RF<-matrix(data_RF,107,107)

label_table<-read.table("topology_labels_for_mean_nt8_ML")
labels<-label_table$V1

col.list<-c("black","blue","aquamarine","gold","darkorchid","darkgoldenrod","darkorange","burlywood1","darkviolet","deeppink","deepskyblue","firebrick","forestgreen","green","lightblue","magenta1","slategray1","pink","tan4","navy","greenyellow","salmon2","mistyrose","mediumaquamarine")
palette(col.list)

fit<-cmdscale(dist_mat_RF,eig=TRUE,k=2)
x<-fit$points[,1]
y<-fit$points[,2]


quartz()
plot(x,y,pch=19,col=labels,xlab="PC 1",ylab="PC 2",main="MDS plot of mean and nt8_ML trees from Rokas et al. based on RF distances")
#legend("bottomleft",legend = levels(labels),fill = col.list, bg = "white",ncol = 2)

# open new window
open3d()
fit_3D<-cmdscale(dist_mat_RF,eig=TRUE,k=3)
x<-fit_3D$points[,1]
y<-fit_3D$points[,2]
z<-fit_3D$points[,3]


plot3d(x,y,z,size=8,col=labels,xlab="PC 1",ylab="PC 2",zlab="PC 3",main="MDS plot of mean and nt8_ML trees from Rokas et al. based on RF distances")

# weighted RF distances
# Read in dissimilarity matrix
data_wRF<-scan("/Users/megan/research/projects/validating_mean_var_out_of_sync_with_office/experiments/2012-10-07_MDS_Rokas_with_mean/diss_wRF_mean_nt8_ML")
dist_mat_wRF<-matrix(data_wRF,107,107)

fit<-cmdscale(dist_mat_wRF,eig=TRUE,k=2)
x<-fit$points[,1]
y<-fit$points[,2]


quartz()
plot(x,y,pch=19,col=labels,xlab="PC 1",ylab="PC 2",main="MDS plot of mean and nt8_ML trees from Rokas et al. based on weighted RF distances")
#legend("bottomleft",legend = levels(labels),fill = col.list, bg = "white",ncol = 2)

fit_3D<-cmdscale(dist_mat_wRF,eig=TRUE,k=3)
x<-fit_3D$points[,1]
y<-fit_3D$points[,2]
z<-fit_3D$points[,3]

open3d()
plot3d(x,y,z,size=8,col=labels,xlab="PC 1",ylab="PC 2",zlab="PC 3",main="MDS plot of mean and nt8_ML trees from Rokas et al. based on weighted RF distances")

# remove trees with long length
data<-scan("/Users/megan/research/projects/validating_mean_var_out_of_sync_with_office/experiments/2012-10-07_MDS_Rokas_with_mean/tree_lengths_mean_nt8_ML")
distances<-matrix(data,107,1)

cutoff_8_dist_mat<-dist_mat_wRF[which(distances<8),which(distances<8)]

fit<-cmdscale(cutoff_8_dist_mat,eig=TRUE,k=2)
x<-fit$points[,1]
y<-fit$points[,2]

quartz()
plot(x,y,pch=19,col=labels[which(distances<8)],xlab="PC 1",ylab="PC 2",main="MDS plot of mean and nt8_ML trees from Rokas et al. with length < 8, weighted RF distance")
legend("bottomleft",legend = levels(labels[which(distances<8)]),fill = col.list, bg = "white",ncol = 2)

# open new window
open3d()

fit_3D<-cmdscale(cutoff_8_dist_mat,eig=TRUE,k=3)
x<-fit_3D$points[,1]
y<-fit_3D$points[,2]
z<-fit_3D$points[,3]


plot3d(x,y,z,size=8,col=labels[which(distances<8)],xlab="PC 1",ylab="PC 2",zlab="PC 3",main="MDS plot of mean and nt8_ML trees from Rokas et al. with length < 8, weighted RF distance")

# Read in dissimilarity matrix
data<-scan("/Users/megan/research/projects/validating_mean_var_out_of_sync_with_office/experiments/2012-10-07_MDS_Rokas_with_mean/diss_mean_nt8_ML")
dist_mat<-matrix(data,107,107)

# reduce the dist_mat to only those rows and columns with length < 8
cutoff_8_dist_mat<-dist_mat[which(distances<8),which(distances<8)]

fit<-cmdscale(cutoff_8_dist_mat,eig=TRUE,k=2)
x<-fit$points[,1]
y<-fit$points[,2]

quartz()
plot(x,y,pch=19,col=labels[which(distances<8)],xlab="PC 1",ylab="PC 2",main="MDS plot of mean and nt8_ML trees from Rokas et al. with length < 8")
legend("bottomleft",legend = levels(labels[which(distances<8)]),fill = col.list, bg = "white",ncol = 2)

# open new window


fit_3D<-cmdscale(cutoff_8_dist_mat,eig=TRUE,k=3)
x<-fit_3D$points[,1]
y<-fit_3D$points[,2]
z<-fit_3D$points[,3]

open3d()
plot3d(x,y,z,size=8,col=labels[which(distances<8)],xlab="PC 1",ylab="PC 2",zlab="PC 3",main="MDS plot of mean and nt8_ML trees from Rokas et al. with length < 8")



