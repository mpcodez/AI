import sys; args = sys.argv[1:]
import math

puzzles = None

with open(args[0]) as file:
    puzzles = file.read().split("\n")

print(puzzles[0] + " G")

gGoal = puzzles[0]
gWidth = 0
gHeight = 0
gSteps = []

gWidth = int(math.sqrt(len(gGoal)))
gHeight = int(len(gGoal)/gWidth)
while len(gGoal)%gWidth != 0:
    gWidth += 1
    gHeight = int(len(gGoal)/gWidth)
    
if gHeight > gWidth:
    tmp = gWidth
    gWidth = gHeight
    gHeight = tmp

class Puzzle():
    def __init__(self, state, goal_state, level, parent = None):
        self.puzzle = state
        self.goal = goal_state
        self.level = level
        self.parent = parent
        self.h()
    
    def puzzle(self):
        return self.puzzle
    
    def goal(self):
        return self.goal
    
    def level(self):
        return self.level
    
    def parent(self):
        return self.parent
    
    def h(self):
        d = 0

        for i in self.puzzle:
            Prow = self.puzzle.index(i)//gWidth
            Pcol = self.puzzle.index(i)%gWidth
            Grow = self.goal.index(i)//gWidth
            Gcol = self.goal.index(i)%gWidth
            d += abs(Grow-Prow) + abs(Gcol-Pcol)
        
        self.hDist = d

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
        if self.tail is None or item[0] < self.head.data[0]:
            # If the queue is empty or the new item has higher priority
            new_node.next = self.head
            self.head = new_node
            if self.tail is None:
                self.tail = new_node
        else:
            current = self.head
            while current.next and item[0] >= current.next.data[0]:
                current = current.next
            new_node.next = current.next
            current.next = new_node
            if new_node.next is None:
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
   
    return (gWidth%2 == 1 and (start_inversions % 2) != (goal_inversions % 2)) or (gWidth%2 == 0 and ((start_inversions+rowOfSpace(start_state_str)) % 2) != ((goal_inversions+rowOfSpace(goal_state_str)) % 2))

def aStar(s, g):
    if is_solvable(s.puzzle, g):
        return []
    
    openSet = Queue()
    openSet.enqueue((s.hDist, s))
    closedSet = {}

    while openSet:
        node = openSet.dequeue()[1]
        
        if node.puzzle in closedSet:
            continue
        
        closedSet[node.puzzle] = node.parent
        
        if node.puzzle == g:
            tmp = closedSet[node.puzzle]
            ret = [node.puzzle]
            while tmp != " ":
                ret.insert(0, tmp)
                tmp = closedSet[tmp]
            return ret
        
        for nbr in neighbors(node.puzzle):
            neighbor = Puzzle(nbr, g, node.level+1, node.puzzle)
            openSet.enqueue((neighbor.hDist+neighbor.level, neighbor))


def compact(path):
    if len(path) == 1:
        return "G"
    retStr = ""
    for i in range(len(path)-1):
        s = rowOfSpace(path[i])
        g = rowOfSpace(path[i+1])
        
        if s == g:
            if path[i].index("_") == path[i+1].index("_")+1:
                retStr += "L"
            else:
                retStr += "R"
                
        elif s == g-1:
            retStr += "D"
        else:
            retStr += "U"
            
    return retStr


for i in range(1, len(puzzles)):
    pzl = Puzzle(puzzles[i], gGoal, 0, " ")
    gSteps = aStar(pzl, gGoal)
    print(puzzles[i] + " " + compact(gSteps))

# Medha Pappula, 6, 2026