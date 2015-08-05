'''
Created on Jul 21, 2015

@author: alkpongsema

- BEAST runs for edges and leaves tests


- Yeast data setup
    - jmodeltest2
    - sampling (without replacement) of genes
    - set up runs for each model
    - Topology splits /comparisons


Model Steps:

1) Run SeqGen (already set up)
2) Model prep
3) Model Run
4) Treeout processing
 a) model based
    - majority/best/consensus
    - edge and leaf extractions
    - leaf norms
  b) general
    - mean
    - base
5) Coordinate discovery
    - logmap
        - topology splits
        - centres
        - coords
            -rooted coords
            -ordered coords
            -all coords
            -all coords ordered
6) Distance calculations
    - between all trees
    - between trees and mean tree
    - between trees and maj/best/con tree
    - between trees and base tree
7) Plotting
    - informative script names/organization
    - topologies
        -logmap
        -MDS
    - all coordinates
        -logmap
        -logmap plus norm
        -MDS 2D
        -MDS 3D
        -plot with ordered colors
    - all models
8) QQ Plotting
    - informative script names/organization
    - between trees and mean tree
    - between trees and maj/best/con tree
    - between trees and base tree
    - individual and all models
'''