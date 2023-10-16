import sys; args = sys.argv[1:]
import math

puzzles = None

with open(args[0]) as file:
    puzzles = file.read().split("\n")

print(puzzles[0] + " G")
gGoal = puzzles[0]


gWidth = int(math.sqrt(len(gGoal)))
gHeight = int(len(gGoal)/gWidth)
while len(gGoal)%gWidth != 0:
    gWidth += 1
    gHeight = int(len(gGoal)/gWidth)
   
if gHeight > gWidth:
    tmp = gWidth
    gWidth = gHeight
    gHeight = tmp

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



class Puzzle:
    puzzle = ""
    goal = ""
    row = 0
    col = 0
    neighbors = []
    dist = 0
    change = "G"
    
    def __init__(self, puzzle, goal, change):
        global gWidth
        self.puzzle = puzzle
        self.goal = goal
        self.row = puzzle.index("_")//gWidth
        self.col = puzzle.index("_")%gWidth
        self.change = change

        d = 0

        for i in puzzle:
            Prow = puzzle.index(i)//gWidth
            Pcol = puzzle.index(i)%gWidth
            Grow = goal.index(i)//gWidth
            Gcol = goal.index(i)%gWidth
            d += abs(Grow-Prow) + abs(Gcol-Pcol)
        
        self.dist = d

    def switch(self, p, smol, big):
        return p[:smol] + p[big] + p[smol+1:big] + p[smol] + p[big+1:]
    
    def getNeighbors(self):
        i = self.puzzle.index("_")
        val1 = Puzzle(self.switch(self.puzzle, (i-gWidth), i), self.goal, "U") if 0 <= i-gWidth else ""
        val2 = Puzzle(self.switch(self.puzzle, i, i+gWidth), self.goal, "D") if len(self.puzzle) > i+gWidth else ""
        val3 = Puzzle(self.switch(self.puzzle, i, i+1), self.goal, "R") if len(self.puzzle) > i+1 and (i+1)%gWidth > (i)%gWidth else ""
        val4 = Puzzle(self.switch(self.puzzle, i-1, i), self.goal, "L") if 0 <= i-1 and (i)%gWidth > (i-1)%gWidth else ""
        self.neighbors = [n for n in [val1, val2, val3, val4] if n != ""]
        return self.neighbors
    
    def getPuzzle(self):
        return self.puzzle
    
    def getChange(self):
        return self.change
    
def BFS(s, g):
       
    if s.puzzle == g.puzzle:
        return "G"

    parseMe = Queue()
    parseMe.enqueue(s)
    dctSeen = {s.puzzle:(s, " ")}

    while parseMe:
        node = parseMe.dequeue()
        for nbr in node.getNeighbors():
            if nbr.puzzle not in dctSeen:
                dctSeen[nbr.puzzle] = (nbr, node.puzzle)
                if nbr.puzzle == g.puzzle:
                    tmp = dctSeen[nbr.puzzle]
                    ret = ""
                    while tmp[1] != " ":
                        ret = tmp[0].change + ret
                        tmp = dctSeen[tmp[1]]
                    return ret
                parseMe.enqueue(nbr)

    return []


gGoal = Puzzle(puzzles[0], puzzles[0], "")


for i in range(1, len(puzzles)):
    gStart = Puzzle(puzzles[i], gGoal.puzzle, "")
    gSteps = BFS(gStart, gGoal)
    print(puzzles[i] + " " + gSteps)

# Medha Pappula, 6, 2026