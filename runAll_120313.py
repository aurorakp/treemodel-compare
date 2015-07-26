#!/usr/bin/env python

# Driver file for the experiments comparing means and variances from MrBayes and bootstrap datasets.

#####  Note:  MrBayes file should be copied into the directory mrbayes_dir when this script finishes running.

import os
import re
import shutil

# parameters
tree_file = 'Hillis_tree.txt'    # rooted but with branch length of 0  (looks unrooted)
seq_dir = 'seqs'
seq_file_prefix = 'seq_'
bp_list = [500,1000,1500,2000]
num_reps = 20

num_raxml_reps = 5
raxml_dir = 'raxml_out'
raxml = 'raxmlHPC_v7.0.4'

#mrbayes_in_dir = 'mrbayes_in'
#mrbayes_out_dir = 'mrbayes_out'
mrbayes_dir = 'mrbayes'
num_iter = 5000000
sampling_rate = 1000
burn_in = 4000000


# Generate 4 sets of sequences for the tree file (lengths 500, 1000, 1500, 2000)
if not os.path.exists(seq_dir):
	os.mkdir(seq_dir)

	# seq-gen [parameters] < [trees] > [sequences]
	# use -o option to present taxa names from being truncated to 10 characters in the output (-on gives NEXUS output)
	# to specify the model: -m <model>  i.e. -m GTR
	# to specify sequence length: -l <sequence_length>
	# to specify number of datasets to simulate: -n <number_of_datasets>
	# to specify the proportion of invariable sites: -i <proportion_invariable>
	# to specify the equilibrium fequencies of A,C,G,T: -f <state_frequencies>
	# to specify the general reversable rate matrix: -r <rate_matrix_values>  (A->C,A->G,A->T,C->G,C->T,G->T)

	# need to change equilibrium frequency of C from 0.3 (in Hillis paper) to 0.31 to get numbers to add to 1 (100)
	for bp in bp_list:	
		os.system('./seq-gen_v1.3.3 -mGTR -l' + str(bp) + ' -n' + str(num_reps) + ' -i0.18 -f0.21,0.31,0.3,0.18 -r1.5,4.91,1.34,0.83,5.8,1 -or < ' + tree_file + ' > ' + seq_dir + '/' + seq_file_prefix + 'bp' + str(bp))

else:
	print('Directory ' + seq_dir + ' already exists - skipping generating sequences')

# Divide up sequence files by replicates.

if not os.path.exists(seq_dir + '/seq_bp' + str(bp_list[0]) + '_rep1'):
	for bp in bp_list:
		seq_source_file = open(seq_dir + '/seq_bp' + str(bp),'r')
		# open the file for the first rep
		rep = 0		
		for line in seq_source_file:
			match_new_rep = re.match(r' 44',line)
			if match_new_rep:
				rep +=1
				# close the old rep file and open the new one
				if (rep > 1):
					rep_file.close()
				rep_file = open(seq_dir + '/seq_bp' + str(bp) + '_rep' + str(rep),'w')
				
			# write the current line to the currently opened rep file
			rep_file.write(line)
		rep_file.close()
		seq_source_file.close()

else:
	print('File ' + seq_dir + '/seq_bp' + str(bp_list[0]) + '_rep1 exists - skipping dividing sequence files')  

# for each set of sequences, run RAxML with bootstrap  (see section 5.1 in RAxML manual, second option)

# RAxML input:  relaxed interleaved or sequential PHYLIP
	# required arguments:
		# -s sequenceFileName     i.e. seq_bp500_rep3
		# -n outputFileName		  i.e. seq_bp500_rep3
		# -m substitutionModel   -m GTRGAMMAI
	
	# optional arguments:
		# -f a    i.e. full analysis, which generates bootstrap trees and ML tree
		# -x 12345   random seed and "invoke novel rapid bootstrapping algorithm"  This is not the usual bootstrapping!  except the introduction of the manual says it is comparable
		# - b randomNumberSeed	for Felsenstein/usual bootstrapping  (randomNumberSeed allows reproducibility)
		# -p randomNumberSeed for parsimony inference; allows reproducibility
		# -N 1000    number of bootstrap trees?
		# -w workingDirectory	i.e. directory to write RAxML output to
		# -k to get branch lengths on the bootstrap trees
		
if not os.path.exists(raxml_dir):
	os.mkdir(raxml_dir)

	# for each sequence file, run RAxML
	for bp in bp_list:
		for rep in xrange(1,num_raxml_reps + 1):
			data_name = 'seq_bp' + str(bp) + '_rep' + str(rep)
			os.system('./' + raxml + ' -s ' + seq_dir + '/' + data_name + ' -n ' + data_name + ' -m GTRGAMMAI -f a -k -x 27362 -p 96618 -N 1000 -w ' + os.getcwd() + '/' + raxml_dir )

else:
	print('Directory ' + raxml_dir + ' exists - skipping running RAxML')

# For each sequence/rep file, create a Nexus file for input into MrBayes
# At the same time, create the MrBayes driver script
#if not os.path.exists(mrbayes_in_dir):
#	os.mkdir(mrbayes_in_dir)

if not os.path.exists(mrbayes_dir):
	os.mkdir(mrbayes_dir)

	for bp in bp_list:
		for rep in xrange(1,num_raxml_reps + 1):
			# Create the Nexus file
			seq_file = 'seq_bp' + str(bp) + '_rep' + str(rep)
			os.system('python phylip2nexus.py ' + seq_dir + '/' + seq_file)
			# the nexus file will end up in the sequence directory.  Move it to mrbayes_in_dir.
#			shutil.move(seq_dir + '/' + seq_file + '.nex',mrbayes_in_dir)
			shutil.move(seq_dir + '/' + seq_file + '.nex',seq_file + '.nex')

			# Create the driver script

			# lset nst=6 rates=invgamma  = use GTR substitution model with gamma-distributed rate 
			#								across sites and a proportion of invariant sites
#			mrBayes_in_file = open(mrbayes_in_dir + '/mrbayes_driver_' + seq_file,'w')
#			mrBayes_in_file = open(mrbayes_dir + '/mrbayes_driver_' + seq_file,'w')
			mrBayes_in_file = open('mrbayes_driver_' + seq_file,'w')

			mrBayes_in_file.write('set autoclose=yes nowarn=yes\n')  # for batch mode  
								#(doesn't ask if want more generations and overwrites files with no warning)
			mrBayes_in_file.write('execute ' + seq_file + '.nex\n')
			mrBayes_in_file.write('lset nst=6 rates=invgamma\n')
			mrBayes_in_file.write('mcmc ngen=' + str(num_iter) + ' samplefreq=' + str(sampling_rate) +'\n')
			mrBayes_in_file.write('sump\n')		# summarize the parameter values
			mrBayes_in_file.write('sumt\n')		# summarize trees; use the default burnin, which is 25%
			mrBayes_in_file.write('quit\n')
			mrBayes_in_file.close()
			
#else:
#	print('Directory ' + mrbayes_in_dir + ' exists - skipping generating the Nexus files and driver scripts') 

# Call MrBayes.  We need to make a new directory for the output, and copy MrBayes into it.
#if not os.path.exists(mrbayes_out_dir):
#	os.mkdir(mrbayes_out_dir)
#	shutil.copy('mb_v3.2.1',mrbayes_out_dir)
#	shutil.copy('mb_v3.2.1',mrbayes_dir)


	for bp in bp_list:
		for rep in xrange(1,num_raxml_reps + 1):
			seq_file = 'seq_bp' + str(bp) + '_rep' + str(rep)
#			os.system(mrbayes_out_dir + '/mb_v3.2.1 < ' + mrbayes_in_dir + '/mrbayes_driver_' + seq_file + ' > mrbayes_out/mrbayes_' + seq_file + '_log.txt &')
#			os.system(mrbayes_dir + '/mb_v3.2.1 < ' + mrbayes_dir + '/mrbayes_driver_' + seq_file + ' > ' + mrbayes_dir + '/mrbayes_' + seq_file + '_log.txt &')
			os.system('./mb_v3.2.1 < mrbayes_driver_' + seq_file + ' > ' + 'mrbayes_' + seq_file + '_log.txt &')

else:
#	print('Directory ' + mrbayes_out_dir + ' exists - skipping running MrBayes')
	print('Directory ' + mrbayes_dir + ' exists - skipping running MrBayes')


