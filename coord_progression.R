bayesCoords <- lapply(1:20, function(i){paste("c:/seqgen/yeast_",i,"_genes1/bayes/yeast_",i,"_genes1_bayes_allcoords.txt",sep="")})
raxmlCoords <- lapply(1:20, function(i){paste("c:/seqgen/yeast_",i,"_genes1/raxml/yeast_",i,"_genes1_raxml_allcoords.txt",sep="")})
beastCoords <- lapply(1:20, function(i){paste("c:/seqgen/yeast_",i,"_genes1/beast/yeast_",i,"_genes1_beast_allcoords.txt",sep="")})
phymlCoords <- lapply(1:20, function(i){paste("c:/seqgen/yeast_",i,"_genes1/phyml/yeast_",i,"_genes1_phyml_allcoords.txt",sep="")})


# Load the coordinate data files:

load.coordsFile <- function(filename){
  d <- read.table(as.character(filename), header = FALSE,colClasses = c("numeric","numeric",rep("NULL",11)),sep=" ")
  #names.coordsData(d)
}

# Give the coordinate data appropriate names:

names.coordsData <- function(coordsData) {
  names(coordsData) <- c("coord1","coord2")
}

# Prepare the color pallette:

colPal<- colorRampPalette(c("blue","green","yellow","red"))(20)

# Plot Progression function:
# 1. Takes the model name
# 2. Takes the directory you want the png files in
# Makes separate plots for each model showing the progression of the topologies
# from blue, green, yellow, and red

plot.progression <- function(model,targetdir){
  setwd(targetdir)
  pngfile = paste(targetdir,"yeast_topo_prog_",model,".png")
  png(pngfile,width=1000,height=1000)
  for (i in 1:20) {
    tempFile =  eval(parse(text=paste(model,"Coords[[",i,"]]",sep="")))
    tempData <- load.coordsFile(tempFile)
    names(tempData) <- c("coords1","coords2")
    if (i !=20){
      if (model == "beast" || model == "phyml"){
        plot.default(tempData$coords1,tempData$coords2,col=c(colPal[i]),xlim=c(-0.15,0.15),ylim=c(-0.15,0.15),xlab="",ylab="")  
      }
      else {
      plot.default(tempData$coords1,tempData$coords2,col=c(colPal[i]),xlim=c(-0.1,0.5),ylim=c(-0.0,0.5),xlab="",ylab="")
      }
      par(new = TRUE)
    }
    else {
      if (model == "beast" || model == "phyml"){
        plot.default(tempData$coords1,tempData$coords2,col=c(colPal[i]),xlim=c(-0.15,0.15),ylim=c(-0.15,0.15),axes=TRUE,xlab="",ylab="")  
      }
      else{
      plot.default(tempData$coords1,tempData$coords2,col=c(colPal[i]),xlim=c(-0.1,0.5),ylim=c(-0.0,0.5),axes=TRUE,xlab="",ylab="")
      }
    }
  
  }
  dev.off()
  
}

# Plot Comparison function:
# 1. Takes the target directory
# Makes a graph comparing the overall output of the different models
# using blue, green, yellow, and red

plot.comparison <- function(targetdir){
  setwd(targetdir)
  pngfile = paste(targetdir,"yeast_topo_comp.png")
  png(pngfile,width=1000,height=1000)
  models <- c("bayes","raxml","beast","phyml")
  compCols = c("blue","green","yellow","red")
  for (j in 1:length(models)){
    for (i in 1:20) {
      model <- models[j]
      tempFile =  eval(parse(text=paste(model,"Coords[[",i,"]]",sep="")))
      tempData <- load.coordsFile(tempFile)
      names(tempData) <- c("coords1","coords2")
      if (i !=20){
        plot.default(tempData$coords1,tempData$coords2,col=c(compCols[j]),xlim=c(-0.15,0.5),ylim=c(-0.15,0.5),xlab="",ylab="")
        
        par(new = TRUE)
      }
      else {
        plot.default(tempData$coords1,tempData$coords2,col=c(compCols[j]),xlim=c(-0.15,0.5),ylim=c(-0.15,0.5),xlab="",ylab="")
        if (j != length(models)){
          par(new = TRUE)
        }
      }
      
      
    }
  }
  dev.off()
}

# Plot Comparison Function with plot.progression coloring
# 1. Takes the target directory
# Colors each topology as in plot.progression to show aggregate trends amongst all
# four models

plot.comparison.progcolors <- function(targetdir) 
{
  setwd(targetdir)
  pngfile = paste(targetdir,"yeast_topo_comp_progcolors.png")
  png(pngfile,width=1000,height=1000)
  models <- c("bayes","raxml","beast","phyml")
  for (j in 1:length(models)){
    for (i in 1:20) {
      model <- models[j]
      tempFile =  eval(parse(text=paste(model,"Coords[[",i,"]]",sep="")))
      tempData <- load.coordsFile(tempFile)
      names(tempData) <- c("coords1","coords2")
      if (i !=20){
        plot.default(tempData$coords1,tempData$coords2,col=c(colPal[i]),xlim=c(-0.15,0.5),ylim=c(-0.15,0.5),xlab="",ylab="")
        
        par(new = TRUE)
      }
      else {
        plot.default(tempData$coords1,tempData$coords2,col=c(colPal[i]),xlim=c(-0.15,0.5),ylim=c(-0.15,0.5),xlab="",ylab="")
        if (j != length(models)){
          par(new = TRUE)
        }
      }
      
      
    }
  }
  dev.off()
}


resultsdir = "c:/seqgen/yeastresults/"

plot.progression("bayes",resultsdir)
plot.progression("raxml",resultsdir)
plot.progression("beast",resultsdir)
plot.progression("phyml",resultsdir)
plot.comparison(resultsdir)
plot.comparison.progcolors(resultsdir)


# Write these graphs up & explanation of them

