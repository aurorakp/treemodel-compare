from subprocess import call

#Trees is the only real input
def main(trees, topology, treeBase):
    groupTrees(trees, topology)
    makeFiles(trees,topology,treeBase)

'''
This program depends on analysis jar if you are running main or groupTrees

main('trees.txt','topology.txt','files/trees.txt')
                                  ^
                    If you are going to make new Files in a seperate
                    directory make sure said directory exists first

'trees.txt' is the name of the file containing the newick files
The program will create the file 'topology.txt' and use it to make files
'''

'''
You do not need analysis.jar

If you already have the 'topology.txt' file then you only need run
makeFiles(same Arguments)
'''


#Do this and the outfile now has a list at the end
#with numbers corresponding to the files the trees will go
def groupTrees(treeFile, output='output.txt'):
    call('java -jar analysis.jar -u -a topology_count -o'.split()+[output,treeFile])
#Seperate into Files
def makeFiles(originalTrees, treeGroups, outputBase):
    groups = openGroups(treeGroups)
    trees = openTrees(originalTrees)
    '''o = open('/Users/dantheman/Desktop/info.txt','w')
    print(trees[:5], trees[-5:], file=o)
    print(groups[:10], groups[-10:], file=o)'''
    if not (groups and trees): return None
    #Seperates outputbase to be able to put the number between
    exten='.'+outputBase.split('.')[-1]
    name = outputBase.replace(exten,'')

    for index in range(len(groups)):
        if groups[index]!=-1:
            f = open('{0}{1}{2}'.format(name,str(groups[index]),exten),'a')
            f.write(trees[index] + "\n")
            '''print(index, groups[index], trees[index], file=o)'''
            f.close()
        '''else:
            print(index, groups[index], trees[index], file=o)
    o.close()'''
#Makes str called groups
def openGroups(groupFile):
    groups = False
    try:
        f = open(groupFile)
        groups = toInts([i for i in f.read().split('\n') if len(i)<5 and len(i)>0])
        f.close()
    except: print("Cannot read Tree Groups file")
    return groups
#Makes list of the trees
def openTrees(treeFile):
    trees = False
    try:
        f = open(treeFile)
        trees = f.read().split('\n')
        trees = [i for i in trees if len(i)>0 and i[0]=='(']
        f.close()
    except: print("Cannot read Original Tree file")
    return trees
#Makes a str[] into a int[]
def toInts(strList):
    return [toInt(i) for i in strList]
def toInt(char):
    try: return int(char)
    except: return -1
