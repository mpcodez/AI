import sys; args = sys.argv[1:]
import math
import time

gStart = ""
gGoal = ""
gWidth = 0
gHeight = 0
gSteps = []

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, item):
        new_node = Node(item)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def dequeue(self):
        if self.is_empty():
            return None
        item = self.head.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        return item

    def is_empty(self):
        return self.head is None

def puzzle(s, g):
    global gStart, gGoal, gWidth, gHeight

    gStart = s
    if g == "":
        l = [*s.replace("_", "")]
        l.sort()
        gGoal = "".join(l) + "_"
    else:
        gGoal = g

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

def count_inversions(puzzle_str):

    inversions = 0
    n = len(puzzle_str)
   
    for i in range(n):
        if puzzle_str[i] == '_':
            continue
        for j in range(i+1, n):
            if puzzle_str[j] == '_':
                continue
            if puzzle_str[i] > puzzle_str[j]:
                inversions += 1
               
    return inversions

def rowOfSpace(st):
    return int(st.index("_")/gWidth)

def is_solvable(start_state_str, goal_state_str):
   
    start_inversions = count_inversions(start_state_str)
    goal_inversions = count_inversions(goal_state_str)
   
    return (gWidth%2 == 1 and (start_inversions % 2) != (goal_inversions % 2)) or (gWidth%2 == 0 and ((start_inversions+rowOfSpace(gStart)) % 2) != ((goal_inversions+rowOfSpace(gGoal)) % 2))

def BFS(s, g):
   
    if is_solvable(s, g):
        return []
       
    if s == g:
        return [s]

    parseMe = Queue()
    parseMe.enqueue(s)
    dctSeen = {s:" "}

    while parseMe:
        node = parseMe.dequeue()
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
                parseMe.enqueue(nbr)

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