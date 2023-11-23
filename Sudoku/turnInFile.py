import sys; args = sys.argv[1:]
import time

INP = ""
PZLSIZE, CSTRSIZE, CSTRS, SYMSET, NBRS = None, None, None, None, None
TOFILL = {}

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
    del newIndSyms[pos]
    TOFILL.discard(pos)
    return pzl[:pos] + sym + pzl[pos + 1:], newIndSyms


def solve(pzl, indSyms):
    global TOFILL

    if "." not in pzl or not indSyms:
        return pzl

    pos = getBestPos(indSyms)

    for sym in indSyms[pos]:
        newPzl, newIndSyms = fowardLooking(pzl, indSyms, pos, sym)
        result = solve(newPzl, newIndSyms)
        if result:
            return result
        else:
            TOFILL.add(pos)
    return ""

def check(pzl):
    for c in CSTRS:
        valSet = {pzl[n] for n in c if pzl[n] != "."}
        valList = [pzl[n] for n in c if pzl[n] != "."]
        if len(valSet) != len(valList):
            return False
    
    return True

if __name__ == "__main__":
    puzzles = open(args[0]).read().split("\n")

    count = 1

    for board in puzzles:
        
        startTime = time.time()
        INP = board
        possibles = setGlobals(board)
        solution = solve(board, possibles)
        
        print(f"{count}: {board}")
        spaces = " "*len(str(count) + ": ")
        print(f"{spaces}{solution} {checkSum(solution)} {round(time.time() - startTime, 2)}s")
        count += 1

# Medha Pappula, 6, 2026