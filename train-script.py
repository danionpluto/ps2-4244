import sys
import math
import re

s = "/Users/danielaramos/Documents/GitHub/ps2-4244/stopwords.txt"
stopwords = []
with open(s, "r") as stop:
   for line in stop:
        line = line.lower()
        split_line = line.strip().split()
        
        for word in split_line:
           stopwords.append(word)
#print(stopwords)

files = sys.argv[1:]
big_doc = {}
bd = {}
lines = []
counts = {}
vocab = {}
classes = {}
i=0
for file in files:
    dash = file.find("-")
    c = file[:dash]
    if c not in classes:
       classes[c] = 1
    else:
       classes[c]+=1
    if c not in big_doc:
       big_doc[c] = {}
    if c not in bd:
       bd[c] = {}
    
    #print("file "+str(i+1) + " "+c)
    with open(file, "r") as in_f:
      for line in in_f:
        line = line.lower()
        split_line = line.strip().split()
        l = []
        for word in split_line:
           if re.match('^[a-zA-Z0-9\-]+$', word) and word not in stopwords:
              l.append(word)
              if word not in counts:
                 counts[word]=1
              else:
                 counts[word] +=1
              if word not in big_doc[c]:
                 big_doc[c][word] = 1
              else:
                 big_doc[c][word] +=1
              if counts[word]>=10:
                 vocab[word] = counts[word]
                 #if word not in bd[c]:
                   # bd[c][word] = 0
                # bd[c][word] = big_doc[c][word]  
                
        #print(split_line)
        #lines.append(l)
    i+=1
#print("vocab\n")
#print(len(vocab))
#print(len(bd["novel"]))
#print(len(bd["info"]))
#print(len(bd["soap"]))
#print("bigdocs\n")
#print(bd)
#print(i)
#print(classes)
#972
count = {}
like = {}
logprior = {}
sum = {}
for c in classes:
   N_doc = i
   N_c = classes[c]
   logprior[c] = math.log2(N_c/N_doc)
   sum[c] = 0
   for w in big_doc[c]:
      if w in vocab:
         sum[c]+=big_doc[c][w]
         
      
   diff = len(vocab)-len(bd[c])
   
   sum[c]+=len(vocab)
   #print(c + str(sum[c]))
   for w in vocab:
      if w in big_doc[c]:
         count[(w,c)] = big_doc[c][w] 
      else:
         count[(w,c)] = 0
         
      
      like[(w,c)] = math.log2((count[(w,c)] +1)/(sum[c]))
# Testing      
#print("bd")
#print(big_doc["novel"]["passing"])
#print("count")
#print(count[("passing","novel")])
#print(bd["novel"])
#print("sum")
#print(sum["novel"])
#print(math.log2((count[("passing","novel")]+1)/(sum["novel"])))
#print(like[("passing", "novel")])
#print(logprior["novel"])

#writing to np.params
with open("nb.params", "w") as out_f:
    for c in logprior.keys():
        out_f.write(c+" PRIOR : "+str(logprior[c])+"\n")
        for w in bd[c]:
           out_f.write(c+" "+w+" "+str(like[(w,c)])+"\n")
           

   