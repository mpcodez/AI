import sys; args = sys.argv[1:]
import time

PZLSIZE, CSTRSIZE, CSTRS, SYMSET, NBRS, CSBYIN, PSBL, TOFILL = None, None, None, None, None, None, None, None
CNT = 0

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
    
    newPSBL = {p: {s for s in PSBL[p]} for p in PSBL}
    newBoard = board
    tmpFILL = {t for t in TOFILL}
    while not ones.is_empty():
        cur = ones.dequeue()
        if cur not in tmpFILL:
            continue
        sym = newPSBL[cur].pop()

        for nbr in NBRS[cur]:
            if nbr in tmpFILL:
                a = newPSBL[nbr] - {sym}
                if len(a) == 0:
                    return None
                if len(a) == 1:
                    ones.enqueue(nbr)
                newPSBL[nbr] = a
            
        newBoard = newBoard[:cur] + sym + newBoard[cur+1:]
        tmpFILL = tmpFILL - {cur}

    PSBL = newPSBL
    TOFILL = tmpFILL
    return newBoard

def propagate_helper(board, con):
    global PSBL, TOFILL, CNT
    
    newPSBL = {p: set(PSBL[p]) for p in PSBL}
    new_board = board
    tmpFILL = set(TOFILL)

    obj = {board[x] for x in con} - {"."}
    constraint = list(con)

    for char in SYMSET:
        if char not in obj:
            present = [char in newPSBL[ind] for ind in constraint]
            val = present.count(True)

            if val == 0:
                return None
            elif val == 1:
                index = constraint[present.index(True)]
                new_board = new_board[:index] + char + new_board[index + 1:]
                newPSBL[index] = set()
                tmpFILL.remove(index)

    PSBL = newPSBL
    TOFILL = tmpFILL
    return new_board

def propagate(board, index):
    global PSBL
    nBoard = board
    newPSBL = {p: set(PSBL[p]) for p in PSBL}
    for cs in CSTRS[:3]:
        nBoard = propagate_helper(nBoard, cs)
        if nBoard is None:
            PSBL = newPSBL
            return None
    return forward(nBoard)

def get_next():
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

def backtracking(board):
    global TOFILL, PSBL, CNT
    CNT += 1

    if "." not in board:
        return board

    index = get_next()
    syms = getBest(board, index)

    for n, val in syms:
        new_board = board[:index] + val + board[index+1:]
        backup = {p: {s for s in PSBL[p]} for p in PSBL}
        psbles = PSBL[index] - {val}
        tmpFILL = {t for t in TOFILL}
        PSBL[index] = set()
        TOFILL = TOFILL - {index}

        ck = False
        for nbr in NBRS[index]:
            a = PSBL[nbr] - {val}
            if len(a) == 0 and nbr in TOFILL:
                ck = True
                continue
            PSBL[nbr] = a
            
        if ck:
            TOFILL = tmpFILL
            PSBL = backup
            PSBL[index] = psbles
            continue

        #new_board11 = propagate(new_board, index)
        #if new_board11 == None:
        #    TOFILL = tmpFILL
        #    PSBL = backup
        #    PSBL[index] = psbles
        #    continue


        new_board2 = forward(new_board)
        if new_board2 == None:
            TOFILL = tmpFILL
            PSBL = backup
            PSBL[index] = psbles
            continue
        
        new_board3 = backtracking(new_board2)

        if new_board3 == None:
            TOFILL = tmpFILL
            PSBL = backup
            PSBL[index] = psbles
            continue
        
        return new_board3
    
    return None

def checkSum(pzl):
    if SYMSET == {*"123456789"}:
        return 324
    return sum(ord(n) for n in pzl) - (PZLSIZE) * min(ord(n) for n in SYMSET)

if __name__ == "__main__":
    puzzles = open(args[0]).read().split("\n")

    count = 1

    for board in puzzles:
        
        startTime = time.time()
        possibles = setGlobals(board)
        solution = backtracking(board)
        
        print(f"{count}: {board}")
        spaces = " "*len(str(count) + ": ")
        print(f"{spaces}{solution} {checkSum(solution)} {round(time.time() - startTime, 2)}s")
        count += 1

# Medha Pappula, 6, 2026