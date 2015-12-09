# treemodel-compare


Summer/Fall 2015 scripts for running, comparing, and visualizing trees and gene evolution in treespace.

<h2> Purpose </h2>

The goal of this repository is intended to display and allow replication of the results in a forthcoming paper on
treespace, tree visualizations, and genetic evolutionary model comparisons by Aurora Koch-Pongsema and Assistant
Professor Megan Owen at CUNY-Lehman College.  For information on the analysis and Sturm_Mean .jar files used to 
calculate geodesic distance and coordinates, and general information on treespace,  please see the publications and 
contact information at <a href="http://comet.lehman.cuny.edu/owen/">Professor Owen's site</a>.  


<h2> Structure </h2>
  
  - *** Note - cleanup and refactoring still in progress ***
  - The "Model" + Obj classes were developed to allow batch processing of gene sequences by their respective modelling 
  programs and provides flags for either the K-80 or the GTR-Gamma/GTR-I-Gamma models to be used.
  - jarutils provides routines to work with the different jars and their functions.
  - Various plotting functions combine Python with R to generate visualizations of treespace under different conditions.
  - BayestoDenali works with output from Mr. Bayes to prepare it for use in Denali.
  - SequenceGenerator 
  

<h2> Work to do </h2>
  - Further results processing
  - Documentation for most scripts
  - Final refactor and code cleanup

<h2> Languages and Dependencies </h2>


<b>Python 2.7</b>
  - <a href="http://biopython.org/">biopython</a>

<b>R 3.2.0 (or higher)</b>
  - <a href = "https://cran.r-project.org/web/packages/plot3D/index.html">plot3D</a>
  
<b> Genetic evolutionary models</b>
  - <a href = "http://mrbayes.sourceforge.net/">Mr. Bayes</a>
  - <a href = "http://sco.h-its.org/exelixis/web/software/raxml/index.html">RAxML</a>
  - <a href = "http://beast2.org/">BEAST2 and BEAUti</a>
  - <a href = "https://github.com/stephaneguindon/phyml/">PhyML</a>
  
<b> Partial dependencies (only certain scripts) </b>
  - <a href = "http://denali.cse.ohio-state.edu/">Denali</a> 
  - <a href = "http://tree.bio.ed.ac.uk/software/seqgen/">Seq-Gen</a> - for sequence generation for simulated data
  
<h2>Contact information</h2>
  - Please contact either Aurora Koch-Pongsema at aurora.koch <i>at</i> lc <i>dot</i> cuny <i>dot</i> edu
  or Professor Megan Owen at megan.owen <i>at</i> lehman <i>dot</i> cuny <i>dot</i> edu for additional information.
  
