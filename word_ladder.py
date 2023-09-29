import sys; args = sys.argv[1:]
import time

startTime = time.time()

wordList = open(args[0]).read().split("\n")
edges = 0
maxDeg = 0
maxWord = ""

def diff(a,b):
    return [a[i]==b[i] for i in range(6)].count(False)==1
    
wDict=[set() for x in range(len(wordList))]
for i in range(len(wordList)-1):
    for y in range(i+1,len(wordList)):
        if diff(wordList[i],wordList[y]):
            edges += 1
            wDict[i].add(wordList[y])
            wDict[y].add(wordList[i])
            
            l1 = len(wDict[i])
            if l1 > maxDeg:
                maxDeg = l1
                
            
print("Word count: " + str(len(wordList)))
print("Edge count: " + str(edges))

counts = [0]*(maxDeg+1)
max2 = ""
for i in range(len(wDict)):
    counts[len(wDict[i])] += 1
    if max2 == "" and len(wDict[i]) == maxDeg-1:
        max2 = wordList[i]
    

print("Degree List: " + str(counts).replace("[", "").replace("]", ""))
print("Construction time: ", str(round(time.time()-startTime, 1)) + "s")
print("Second degree word: " + max2)

visited = [False]*len(wordList)
count = 0

def visit(l):
    visited[wordList.index(i)] = True
    

components = []

for i in wordList:
    
    

# Medha Pappula, 6, 2026