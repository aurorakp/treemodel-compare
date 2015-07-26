'''
Created on Jun 5, 2015

@author: alkpongsema
'''
'''
if __name__ == '__main__':
    generations = []
    likelihoods = []
    trees = []
    treeNum = 3
    
    # Handle the .t run file:
       
    t_length = 1
    t_file = open('intest.txt','r')
    
    # Measure the length of the t file
    for line in t_file:
        t_length = t_length + 1
    t_file.close()
    
    # Process the t file for the desired number of trees by filling the appropriate
    # lists starting treeNum from file end, subtracting 1 for the "end;" line
    t_file = open('intest.txt','r')
    t_start = t_length - treeNum -1  
    t_counter =1
    
    for line in t_file:
        if (t_counter < t_start):
            t_counter = t_counter + 1
        else:
            t_counter = t_counter + 1
            temp = line.split()
            if temp[0] != "end;" and temp[0] != "":
                trees.append(temp[4].strip())
        
    t_file.close()
    
    
    p_file = open('in2test.txt','r')
    p_length = 1
    for line in p_file:
        p_length = p_length + 1
    p_file.close()
    
    p_file = open('in2test.txt','r')
    p_start = p_length - treeNum

    p_counter = 1
    for line in p_file:
        if (p_counter < p_start):
            p_counter = p_counter + 1
        elif (p_counter >= p_start):
            p_counter = p_counter + 1
            temp = line.split()
            generations.append(temp[0].strip())
            likelihoods.append(temp[1].strip())

    p_file.close()
    
       
    #print generations
    #print likelihoods
    #print trees
 
        
    
    outfile = open('out2test.txt','w')
    for i in range(treeNum):
        outfile.write(generations[i]+" "+likelihoods[i]+" " + trees[i] + "\n")
        
'''        