import math
import time

INP = ""
PZLSIZE, CSTRSIZE, CSTRS, SYMSET, NBRS = None, None, None, None, None
TOFILL = {}
CNT = 0
ONES = set()

def setGlobals(board):
    global PZLSIZE, CSTRSIZE, CSTRS, SYMSET, NBRS, TOFILL
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
    NBRS = [set().union(*[cset for cset in CSTRS if n in cset]) - {n} for n in range(PZLSIZE)]
    psbl = {index: (SYMSET - {INP[n] for n in NBRS[index]}) if INP[index] == '.' else set() for index in range(PZLSIZE)}
    ONES = {index for index in TOFILL if len(psbl[index]) == 1}
    TOFILL = {index for index, value in enumerate(board) if value == '.'}
    return psbl

def checkSum(pzl):
    if SYMSET == {*"123456789"}:
        return 324
    return sum(ord(n) for n in pzl) - (PZLSIZE) * min(ord(n) for n in SYMSET)

def getBestPos(indSyms):
    global TOFILL
    return min(TOFILL, key=lambda pos: len(indSyms[pos]))

def fowardLooking(pzl, indSyms, pos, sym):
    newIndSyms = {p: {s for s in indSyms[p]} for p in indSyms}
    for nbr in NBRS[pos]:
        if nbr not in indSyms and pzl[nbr] == sym:
            continue
        if nbr in indSyms:
            newIndSyms[nbr].discard(sym)
    newIndSyms[pos] = set()
    TOFILL.discard(pos)
    return pzl[:pos] + sym + pzl[pos + 1:], newIndSyms


def constraintProp(pzl, indSyms):
    global TOFILL
    new_syms = {p: {s for s in indSyms[p]} for p in indSyms}
    newPZL = pzl
    changed = set()
    for cs in CSTRS:
        tmp = list(cs)
        objects = [newPZL[index] for index in tmp]
        for symbol in SYMSET:
            if symbol not in objects:
                present = [symbol in new_syms[index] for index in tmp]
                if present.count(True) == 0:
                    TOFILL = TOFILL.union(changed)
                    return pzl, indSyms, None
                if present.count(True) == 1:
                    index = tmp[present.index(True)]
                    newPZL = newPZL[:index] + symbol + newPZL[index + 1:]
                    new_syms[index] = set()
                    changed.add(index)
                    TOFILL.discard(index)

    return newPZL, new_syms, changed

def solve(pzl, indSyms):
    global TOFILL

    if "." not in pzl:
        return pzl
    
    if indSyms == None:
        return None
    

    pzl, indSyms, changed = constraintProp(pzl, indSyms)
    

    pos = getBestPos(indSyms)

    for sym in indSyms[pos]:
        newPzl, newIndSyms = fowardLooking(pzl, indSyms, pos, sym)
        result = solve(newPzl, newIndSyms)
        if result:
            return result
        else:
            TOFILL.add(pos)

    if changed is not None:
        TOFILL = TOFILL.union(changed)
    return None

board = "....5.6.1.....4..5..8.........4.7.2..6......3.....8...15.........2....7........8."
INP = board
sT = time.time()
possibles = setGlobals(board)
sol = solve(board, possibles)
#print(check(sol))
print(sol)
print((time.time()-sT))
print(checkSum(sol))
print(CNT)