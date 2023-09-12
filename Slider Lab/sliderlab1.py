import sys;args=sys.argv[1:]
import math 
import time

gStart = ""
gGoal = ""
gWidth = 0
gHeight = 0
gSteps = []

def puzzle(s, g):
    global gStart, gGoal, gWidth, gHeight

    gStart = s
    l = [*s.replace("_", "")]
    l.sort()
    gGoal = "".join(l) + "_" if g == "" else g

    gWidth = int(math.sqrt(len(s)))
    gHeight = int(len(s)/gWidth)
    while len(s)%gWidth != 0:
        gWidth += 1
        gHeight = int(len(s)/gWidth)
    
    if gHeight > gWidth:
        tmp = gWidth
        gWidth = gHeight
        gHeight = tmp
    
def neighbors(p):
    i = p.index("_")
    val1 = switch(p, (i-gWidth), i) if 0 <= i-gWidth else ""
    val2 = switch(p, i, i+gWidth) if len(p) > i+gWidth else ""
    val3 = switch(p, i, i+1) if len(p) > i+1 and (i+1)%gWidth > (i)%gWidth else ""
    val4 = switch(p, i-1, i) if 0 <= i-1 and (i)%gWidth > (i-1)%gWidth else ""
    ret = set([val3, val4, val1, val2])
    ret.discard("")
    return list(ret)
    
def switch(p, smol, big):
    return p[:smol] + p[big] + p[smol+1:big] + p[smol] + p[big+1:]

def output(p):
    for i in range(0, len(p), 5):
        band(p[i:i+5 if i+5 < len(p) else len(p)])
        print("")
    
def band(p):
    for i in range(gHeight):
        val = ""
        for x in p:
            val += " ".join([*x[i*gWidth:i*gWidth + gWidth]]) + "   "
        print(val.strip())

def BFS(s, g):
    if s == g:
        return [s]

    parseMe = [s]
    dctSeen = {s:" "}

    while parseMe:
        node = parseMe.pop(0)
        for nbr in neighbors(node):
            if nbr not in dctSeen.keys():
                dctSeen[nbr] = node
                if nbr == gGoal:
                    tmp = dctSeen[nbr]
                    ret = [nbr]
                    while tmp != " ":
                        ret.insert(0, tmp)
                        tmp = dctSeen[tmp]
                    return ret
                parseMe.append(nbr)

    return []

startTime = time.time()

if len(args) == 2:
    puzzle(args[0], args[1])
else:
    puzzle(args[0], '')

gSteps = BFS(gStart, gGoal)
output(gSteps if gSteps != [] else [gStart])
print(f"Steps: {len(gSteps)-1}")
print("Time:", str(round(time.time()-startTime, 2)) + "s")
# Medha Pappula, 6, 2026