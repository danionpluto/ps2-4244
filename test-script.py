
import sys
import math
import re


classes = []
#wordc = {}
vocab = []
sums = {}
logs = {}
ranks = {}
with open(sys.argv[1], "r") as model:
      for line in model:
        split_line = line.strip().split()
        c = split_line[0]
        word = split_line[1]
        if c not in classes:
            classes.append(c)  
        if word!="PRIOR:":
            vocab.append(word)
        if c not in ranks:
            ranks[c] = {}
        if word!="PRIOR":
            ranks[c][word] = float(split_line[2])
            logs[(word,c)] = (float(split_line[2]))

words = []      
wordcount ={}
#open the test file, store the words in array words, and the counts of each word in dict wordcount
with open(sys.argv[2], "r") as test:
      for line in test:
        line = line.lower()
        split_line = line.strip().split()
        for word in split_line:
                    words.append(word)
                    if word not in wordcount:
                        wordcount[word] = 1
                    else:
                        wordcount[word]+=1
                    


#this dictionary will store the denominators for each class to use in the proportion claculations
denom = {}
for c in classes:
    #calculate denom for each class that will be used in proportion calculations
    tot = 0      
    for w in words:
       if w in ranks[c]:
          tot += 2**ranks[c][w]
    denom[c] = tot
    #initialize the prob sum to the value of the logprior
    sums[c] = float(logs[("PRIOR:", c)])
    #Add to the prob sum the log liklehoods of each word in the test file
    for word in words:  
        if (word, c) in logs:
            a = float(logs[(word,c)])
        else:
            a = 0
        sums[c]+= a
                    

weights = {}
# calculate and store the numerators for each proportion calc
for c in classes:
    weights[c] = {}
    for w in wordcount:
        if w in ranks[c]: 
            if w not in weights[c]:
                weights[c][w] = 0
            weights[c][w] += (wordcount[w] * 2**logs[(w,c)])
            
    # calculate proportions
    for w in weights[c]:
        weights[c][w] = math.log2(weights[c][w] / denom[c])
    

#print output
print("Class of test: " + max(sums, key=sums.get))
for c in ranks:
    print(c + ": "+str(sums[c]))
    i = 0
    while i<15:
        word = max(weights[c], key=weights[c].get)
        print(c + " "+ str(i)+ " : "+ word + " "+ str(weights[c][word]))
        del weights[c][word]
        i+=1
    

