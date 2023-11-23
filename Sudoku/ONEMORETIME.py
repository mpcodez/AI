import time


PZLSIZE, CSTRSIZE, CSTRS, SYMSET, NBRS, CSBYIN, PSBL, TOFILL = None, None, None, None, None, None, None, None

def setGlobals(board):
    global PZLSIZE, CSTRSIZE, CSTRS, SYMSET, NBRS, CSBYIN, PSBL, TOFILL
    INP = board
    pzl = ''.join([n for n in board if n != '.'])

    PZLSIZE = len(INP)
    CSTRSIZE = int(len(INP) ** .5)
    N = PZLSIZE ** .5

    subheight = -1
    i = int(N ** .5)
    while i < N and subheight == -1:
        if N % i == 0:
            subheight = i
        i += 1
    subwidth = int(N // subheight)

    SYMSET = {*pzl} - {'.'}
    if len(SYMSET) != CSTRSIZE:
        otherSyms = [n for n in '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ0']
        while len(SYMSET) < CSTRSIZE:
            SYMSET.add(otherSyms.pop(0))

    rowcstr = [{index for index in range(row * CSTRSIZE, (row + 1) * CSTRSIZE)}
               for row in range(CSTRSIZE)]
    colcstr = [{index for index in range(col, col + PZLSIZE - subwidth * subheight + 1, subwidth * subheight)}
               for col in range(CSTRSIZE)]
    subcstr = [{boxRow + boxColOffset + subRow * CSTRSIZE + subCol
                for subRow in range(subheight) for subCol in range(subwidth)}
               for boxRow in range(0, PZLSIZE, subheight * CSTRSIZE) for boxColOffset in range(0, CSTRSIZE, subwidth)]
    
    CSTRS = rowcstr + colcstr + subcstr

    CSBYIN = [[cset-{n} for cset in CSTRS if n in cset] for n in range(PZLSIZE)]
    NBRS = [set().union(*[cset for cset in CSTRS if n in cset]) - {n} for n in range(PZLSIZE)]
    PSBL = {index: (SYMSET - {INP[n] for n in NBRS[index]}) if INP[index] == '.' else set() for index in range(PZLSIZE)}
    TOFILL = {index for index, value in enumerate(board) if value == '.'}

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

def forward(board):
    global PSBL, TOFILL
    ones = Queue()
    for index in TOFILL:
        if len(PSBL[index]) == 1:
            ones.enqueue(index)

    
    
    while not ones.is_empty():
        cur = ones.dequeue()
        sym = PSBL[cur].pop()
        newPSBL = {p: {s for s in PSBL[p]} for p in PSBL}

        for nbr in NBRS[cur]:
            a = newPSBL[nbr] - {sym}
            if len(a) == 0:
                return None
            if len(a) == 1:
                ones.enqueue(nbr)
            newPSBL[nbr] = a

        PSBL = newPSBL
        board = board[:cur] + sym + board[cur+1:]
        TOFILL = TOFILL - {cur}

    return board

"""
def propagate_helper(board, con):
    for c in con:
        for char in PSBL[c]:
            if char only appears once, place it
    return new_board

def propagate(board):
    call propagate helper 3 times, passing board and each different constraint set, returning none if none is returned
    return forward(board)
"""

def get_next(board):
    global TOFILL, PSBL
    return min(TOFILL, key=lambda pos: len(PSBL[pos]))

def getBest(board, ind):
    global PSBL
    lst = []

    for p in PSBL[ind]:
        tmp = 0
        for i in NBRS[ind]:
            if board[i] == p:
                tmp = 1000000000000
                break
            if p in PSBL[i]:
                tmp += 1
        lst.append((tmp, p))
    
    lst = sorted(lst)
    return lst


def check(pzl):

    for c in CSTRS:
        valSet = {pzl[n] for n in c if pzl[n] != "."}
        valList = [pzl[n] for n in c if pzl[n] != "."]
        if len(valSet) != len(valList):
            return False
    
    return True

def backtracking(board):
    global TOFILL

    if not check(board):
        return None
    
    if "." not in board:
        return board
    

    var = get_next(board)
    syms = getBest(board, var)

    for n, val in syms:
        new_board = board[:var] + val + board[var+1:]
        psbles = PSBL[var] - {val}
        PSBL[val] = set()
        TOFILL = TOFILL - {var}
        
        new_board2 = forward(new_board)
        if new_board2 == None:
            TOFILL.add(var)
            PSBL[val] = psbles
            continue

        new_board3 = backtracking(new_board2)

        if new_board3 == None:
            TOFILL.add(var)
            PSBL[val] = psbles
            continue
        
        return new_board3
    
    return None

sT = time.time()
board = "...9....8.4.2189...3....72.3.4.......2.....9.......5.2.67....1...8147.3.4....2..."
setGlobals(board)
s = backtracking(board)
print(s)
print(s == "958761324721943856436825179684132597517496238392587461145279683873654912269318745")
print((time.time()-sT))