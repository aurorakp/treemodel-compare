library(ape)

topomatch <- function(t1, t2){
  
  tree1 <- read.tree(text = t1)
  tree2 <- read.tree(text = t2)
  treeEqual <- all.equal(tree1,tree2)
  treeEqual
}