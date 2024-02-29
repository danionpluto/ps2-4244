
import sys
import math
import re
files = sys.argv[1:]
i = 1

classes = []
vocab = []
sums = {}
logs = {}
with open(sys.argv[1], "r") as model:
      for line in model:
        split_line = line.strip().split()
        l = []
        c = split_line[0]
        word = split_line[1]
        if c not in classes:
            classes.append(c)
        
        
        elif word not in vocab and word!="PRIOR":
            vocab.append(word)
        
        logs[(word,c)] = split_line[2]

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
                    if (word, c) in logs:
                        a = float(logs[(word,c)])
                    else:
                        a = 0
                    sums[c]+= a

            



print(sums)        


  
