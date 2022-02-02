import sys
sys.setrecursionlimit(10000)
#---------------------
#Read Kmers from file and convert it into Kmers-1 then save it dictionary
#---------------------
def ReadfromFile(Filename):
    FR_dict = {}
    gapLen = -1
    with open(Filename) as f:
        Kmer_gapLen = f.readline().rstrip().split(' ')
        KmersLen, gapLen = int(Kmer_gapLen[0]), int(Kmer_gapLen[1])
        Kmers = f.readlines()
    for Kmer in Kmers:
        forward, backward = Kmer.split('|')
        backward = backward.rstrip()
        
        key = forward[:-1] + "-" + backward[:-1]
        value = forward[1:] + "-" + backward[1:]
        
        if (key in FR_dict.keys()):
            FR_dict[key].append(value)
        else:
            FR_dict[key] = [value]

    return KmersLen, gapLen, FR_dict

#---------------------
#find Start of Kmers-1
#---------------------
def findStart(FR_dict):
    for key in FR_dict.keys(): 
        existKey = False
        for valList in FR_dict.values():
            if ( key in valList ):
                existKey = True
                break
    
        if (not existKey):
            start = key
            break
        
    return start

#---------------------    
#creat connceted graph
#---------------------    
def FindPath(startKey, FR_dict):
    Key = startKey
    path=[]
    if (Key in FR_dict.keys()):
        for value in FR_dict[Key]:
            FR_dict[Key].remove(value)
            path = FindPath(value, FR_dict)
            path.append(value) 
        return path
    return path

#---------------------    
#Take the first charachter from prefix and the last Kmer-1 of the prefix
#Take the first charachter from suffix and the last Kmer-1 of the suffix
#---------------------
def findPrefixSuffix(path, end):
    prefix, suffix= "", ""

    for val in path:
        forward, reverse = val.split('-')
        
        #if the loop reach to the final word take it all
        if (val == end):
            prefix += forward
            suffix += reverse
        
        #else take the first charachter       
        else:
            prefix += forward[0]
            suffix += reverse[0]
            
    return prefix, suffix
   
#---------------------    
#Write the sequence (Prefix + (last K+d)suffix)
#---------------------
def getSequence(prefix, suffix, gapLen, kmersLen):
    lastKD = gapLen + kmersLen
    sequence = prefix + suffix[-lastKD:]

    return sequence  

#Main 
KmersLen, gapLen, FR_dict = ReadfromFile("testKmersPaired.txt")
start = findStart(FR_dict)

path = FindPath(start, FR_dict)  
path.append(start)
path = path[::-1]

end = path[-1]
prefix, suffix = findPrefixSuffix(path, end)
sequence = getSequence(prefix, suffix, gapLen, KmersLen)
print (sequence)


    
    
    
    