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

k2 = 0
k3 = 0
k4 = 0

def pairs(ind):
    global k2
    p1 = ind
    p2 = wordList.index(list(wDict[ind])[0])
    if len(wDict[p1]) == len(wDict[p2]) == 1 and wordList[p1] in list(wDict[p2]) and wordList[p2] in list(wDict[p1]):
        k2 += 1


def triples(ind):
    global k3
    p1 = ind
    p2 = wordList.index(list(wDict[ind])[0])
    p3 = wordList.index(list(wDict[ind])[1])
    print("")
    print(wDict[p1])
    print(wDict[p2])
    print(wDict[p3])
    if (len(wDict[p1]) == len(wDict[p2]) == len(wDict[p3]) == 2) and (wordList[p1] in list(wDict[p2])) and (wordList[p2] in list(wDict[p1])) and (wordList[p3] in list(wDict[p2])) and (wordList[p2] in list(wDict[p3])) and (wordList[p1] in list(wDict[p3])) and (wordList[p3] in list(wDict[p1])):
        k3 += 1
        print("True")
    
    print("")
    pass

def quadruples(ind):
    global k4
    pass

counts = [0]*(maxDeg+1)
max2 = ""
for i in range(len(wDict)):
    ln = len(wDict[i])
    counts[ln] += 1
    if max2 == "" and ln == maxDeg-1:
        max2 = wordList[i]
    if ln == 1:
        pairs(i)
    

print("Degree List: " + str(counts).replace("[", "").replace("]", ""))
print("Construction time: ", str(round(time.time()-startTime, 1)) + "s")
print("Second degree word: " + max2)

visited = [False]*len(wordList)
components = []
count = 0

def visit(l):
    global visited
    ind = wordList.index(l)
    if visited[ind] == True:
        return ""
    else:
        visited[ind] = True
        components[count].add(wordList[ind])
        for i in wDict[ind]:
            components[count].add(i)
            visit(i)
        return ""

index = 0
while all(visited) == False:
    index = visited.index(False)
    components.append(set())
    visit(wordList[index])
    count += 1

unique = {len(i) for i in components}

print("Connected component size count: " + str(len(unique)))
print("Largest component size: " + str(max(unique)))
print("K2 count: " + str(int(k2/2)))
print("K3 count: " + str(int(k2/3)))

# Medha Pappula, 6, 2026