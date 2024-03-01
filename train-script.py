import sys
import math
import re

s = "/Users/danielaramos/Documents/GitHub/ps2-4244/stopwords.txt"

#open and tokenize stopwords.txt
stopwords = []
with open(s, "r") as stop:
   for line in stop:
        line = line.lower()
        split_line = line.strip().split()
        
        for word in split_line:
           stopwords.append(word)

#open each training file and change class counts accordingly
files = sys.argv[1:]
big_doc = {}
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
    
    
    #print("file "+str(i+1) + " "+c)
    with open(file, "r") as in_f:
      for line in in_f:
        line = line.lower()
        split_line = line.strip().split()
        l = []
        for word in split_line:
           if re.match('^[a-zA-Z0-9\-]+$', word) and word not in stopwords:
              l.append(word)
              #add to the count of word in counts
              if word not in counts:
                 counts[word]=1
              else:
                 counts[word] +=1
              #add to the count of the word in the speciific class the file falls under
              if word not in big_doc[c]:
                 big_doc[c][word] = 1
              else:
                 big_doc[c][word] +=1
              # add word and its counts to dictionary vocab, if and only if its count is greater than or equal to 10
              if counts[word]>=10:
                 vocab[word] = counts[word]
                 
    i+=1

count = {}
like = {}
logprior = {}
sum = {}
for c in classes:
   N_doc = i
   N_c = classes[c]
   #calculate the class log prior
   logprior[c] = math.log2(N_c/N_doc)
   #calculate the total counts of a word in a class
   sum[c] = 0
   for w in big_doc[c]:
      if w in vocab:
         sum[c]+=big_doc[c][w]
         
      
   
   #add smoothing by adding length of the vocab
   sum[c]+=len(vocab)
   #calculate and store the log liklehood for each word
   for w in vocab:
      if w in big_doc[c]:
         count[(w,c)] = big_doc[c][w] 
      else:
         count[(w,c)] = 0
         
      
      like[(w,c)] = math.log2((count[(w,c)] +1)/(sum[c]))
#write to np.params
with open("nb.params", "w") as out_f:
    for c in logprior.keys():
        out_f.write(c+" PRIOR: "+str(logprior[c])+"\n")
        for w in vocab:
            out_f.write(c+" "+w+" "+str(like[(w,c)])+"\n")
           
           

   