source("topomatch.R")

treeNum <- 20

bayesfiles <- lapply(1:20,function(i){paste("c:/seqgen/yeasttopodata/yeast_",i,"_bayes_toposummary.txt",sep="")})
raxmlfiles <- lapply(1:20,function(i){paste("c:/seqgen/yeasttopodata/yeast_",i,"_raxml_toposummary.txt",sep="")})
beastfiles <- lapply(1:20,function(i){paste("c:/seqgen/yeasttopodata/yeast_",i,"_BEAST_toposummary.txt",sep="")})
phymlfiles <- lapply(1:20,function(i){paste("c:/seqgen/yeasttopodata/yeast_",i,"_phyml_toposummary.txt",sep="")})


load.file <- function(filename){
  d <- read.table(as.character(filename), header = TRUE, colClasses=c("character","numeric"),sep=" ")
}

checkTopo <- function(simname, fileNum1, fileNum2, topoNum1, topoNum2){
  if (simname == "bayes"){
    a <- load.file(bayesfiles[fileNum1])
    b <- load.file(bayesfiles[fileNum2])
    sametree <- topomatch(a[topoNum1,1],b[topoNum2,1])
    sametree
  }
  else if (simname == "raxml"){
    a <- load.file(raxmlfiles[fileNum1])
    b <- load.file(raxmlfiles[fileNum2])
    sametree <- topomatch(a[topoNum1,1],b[topoNum2,1])
    sametree
  }
  else if (simname == "beast"){
    a <- load.file(beastfiles[fileNum1])
    b <- load.file(beastfiles[fileNum2])
    sametree <- topomatch(a[topoNum1,1],b[topoNum2,1])
    sametree
  }
  else if (simname == "phyml"){
    a <- load.file(phymlfiles[fileNum1])
    b <- load.file(phymlfiles[fileNum2])
    sametree <- topomatch(a[topoNum1,1],b[topoNum2,1])
    sametree
  }
  
}

# want to make a record of which topology is the 'dominant' one to see if we can find
# convergence/consistency

# and track the 'matching' topology if it's not the dominant one

# check if Topo #1 is the same as the first topo in the others
firstTopoSame <- lapply(1:20,function(i){checkTopo(1,i,1,1)})
# check if Topo #1 is the same as the second topo in the others
secondTopoSame <- lapply(1:20,function(i){checkTopo(1,i,2,1)})

y1 <- load.file(bayesfiles[1])
y2 <- load.file(raxmlfiles[1])
y3 <- load.file(beastfiles[1])
y4 <- load.file(phymlfiles[1])

# We're interested in the dominant topology at the 'end':

topoPick <- 1

bayesTopoMatched <- data.frame(x=rep(NA,20),y=rep(NA,2))
colnames(bayesTopoMatched) <- c(y1[1,1],y1[2,1])
bayesfirstTopoSame <- lapply(1:20,function(i){checkTopo("bayes",topoPick,i,1,1)})
bayessecondTopoSame <- lapply(1:20,function(i){checkTopo("bayes",topoPick,i,2,1)})

for (i in 1:20) {
  
  bayesTopoMatched[i,1] <- bayesfirstTopoSame[i]
  bayesTopoMatched[i,2] <- bayessecondTopoSame[i]
  }
raxmlTopoMatched <- data.frame(x=rep(NA,20),y=rep(NA,2))
colnames(raxmlTopoMatched) <- c(y2[1,1],y2[2,1])
raxmlfirstTopoSame <- lapply(1:20,function(i){checkTopo("raxml",topoPick,i,1,1)})
raxmlsecondTopoSame <- lapply(1:20,function(i){checkTopo("raxml",topoPick,i,2,1)})

for (i in 1:20) {
  raxmlTopoMatched[i,1] <- raxmlfirstTopoSame[i]
  raxmlTopoMatched[i,2] <- raxmlsecondTopoSame[i]
}
beastTopoMatched <- data.frame(x=rep(NA,20),y=rep(NA,2))
colnames(beastTopoMatched) <- c(y3[1,1],y3[2,1])
beastfirstTopoSame <- lapply(1:20,function(i){checkTopo("beast",topoPick,i,1,1)})
beastsecondTopoSame <- lapply(1:20,function(i){checkTopo("beast",topoPick,i,2,1)})

for (i in 1:20) {
  
  beastTopoMatched[i,1] <- beastfirstTopoSame[i]
  beastTopoMatched[i,2] <- beastsecondTopoSame[i]
}
phymlTopoMatched <- data.frame(x=rep(NA,20),y=rep(NA,2))
colnames(phymlTopoMatched) <- c(y4[1,1],y4[2,1])
phymlfirstTopoSame <- lapply(1:20,function(i){checkTopo("phyml",topoPick,i,1,1)})
phymlsecondTopoSame <- lapply(1:20,function(i){checkTopo("phyml",topoPick,i,2,1)})

for (i in 1:20) {
  
  phymlTopoMatched[i,1] <- phymlfirstTopoSame[i]
  phymlTopoMatched[i,2] <- phymlsecondTopoSame[i]
}


bayesMatchOut <- paste("c:/seqgen/yeasttopodata/yeast_bayes_",topoPick,"_topomatches.txt",sep="")
raxmlMatchOut <- paste("c:/seqgen/yeasttopodata/yeast_raxml_",topoPick,"_topomatches.txt",sep="")
beastMatchOut <- paste("c:/seqgen/yeasttopodata/yeast_beast_",topoPick,"_topomatches.txt",sep="")
phymlMatchOut <- paste("c:/seqgen/yeasttopodata/yeast_phyml_",topoPick,"_topomatches.txt",sep="")

write.table(bayesTopoMatched,file=bayesMatchOut,col.names=TRUE,sep=" ")
write.table(raxmlTopoMatched,file=raxmlMatchOut,col.names=TRUE,sep=" ")
write.table(beastTopoMatched,file=beastMatchOut,col.names=TRUE,sep=" ")
write.table(phymlTopoMatched,file=phymlMatchOut,col.names=TRUE,sep=" ")

# as adding in new genes, how is that changing the distribution (narrower? rounder?)
# logmap according to a specific topology (topo2 for the ones where topo1 is not dominant)
# assemble dominant, 2nd place etc. topologies into a table  
