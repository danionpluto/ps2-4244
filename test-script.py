
import sys
import math
import re
files = sys.argv[1:]
i = 1

classes = []
wordc = {}
vocab = []
sums = {}
logs = {}
ranks = {}
with open(sys.argv[1], "r") as model:
      for line in model:
        split_line = line.strip().split()
        l = []
        c = split_line[0]
        word = split_line[1]
        if c not in classes:
            classes.append(c)
        
        
        if word!="PRIOR:":
            vocab.append(word)
        if c not in ranks:
            ranks[c] = {}
        if word!="PRIOR":
            ranks[c][word] = split_line[2]
            logs[(word,c)] = (float(split_line[2]))

#print(vocab)       
wordcount ={}
#print(logs)
for c in classes:
    sums[c] = float(logs[("PRIOR:", c)])
    with open(sys.argv[2], "r") as test:
      for line in test:
        line = line.lower()
        split_line = line.strip().split()
        for word in split_line:
            if re.match('^[a-zA-Z0-9\-]+$', word):
                
                if word in vocab:
                    if word not in wordcount:
                        wordcount[word] = 1
                    else:
                        wordcount[word]+=1
                    if (word, c) in logs:
                        a = float(logs[(word,c)])
                    else:
                        a = 0
                    sums[c]+= a
#print(wordcount["PRIOR"])
#print("PRIOR" in vocab)
weights = {}   
words = {}
#print(vocab)                 
for c in ranks:
    r = {}
    denom = 0
    for w in wordcount.keys():
        #print(w)
        if w in ranks[c] and w in wordcount:
            denom += float(ranks[c][w])*wordcount[w]
     
    for w in ranks[c]:
        if w in vocab:
            if w in ranks[c] and w in wordcount:
                r[w] = float(ranks[c][w])*wordcount[w]/denom
    
    words[c] = sorted(r, reverse = True)
    weights[c] = r
    print(weights[c])
            
#print(ranks["novel"]["great"])

#print("Class of test: " + max(sums))
#for c in ranks:
    #print(c + ": "+str(sums[c]))
    #features = sorted(ranks[c])
    #print(features)
    #i = 0
   # while i<15:
        #print(c + " "+ str(i+1)+ " : "+ features[i] + " "+ ranks[c][features[i]])
       # i+=1

print("Class of test: " + max(sums, key=sums.get))
for c in ranks:
    print(c + ": "+str(sums[c]))
    i = 0
    while i<15:
        print(c + " "+ str(i)+ " : "+ str(words[c][i]) + " "+ str(weights[c][words[c][i]]))
        i+=1
        

  
