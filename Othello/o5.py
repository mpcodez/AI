import sys; args = sys.argv[1:]

args = ["oooo.ooo.ooooooo.ooooxoooooxoo.oooxxxoo.oooxxxx.oooooxx.ooooo...", "x"]

startboard = args[0].lower() if len(args) > 0 else '.'*27 + 'ox......xo' + '.'*27
startTkn = args[1].lower() if len(args) > 1 else {0:'x', 1:'o'}[startboard.count('.')%2]
oppTkn = "x" if startTkn == "o" else "o"
nbrFlips = {}
nbrMoves = {}
SUBSETS = []
TKNSETS = {}
SAFE_EDGES = {0: {1,2,3,4,5,6,7,8,16,24,32,40,48,56}, 7: {0,1,2,3,4,5,6,15,23,31,39,47,55,63},
     56: {0,8,16,24,32,40,48,57,58,59,60,61,62,63}, 63: {7,15,23,31,39,47,55,56,57,58,59,60,61,62}}
EDGE_CNR = {edgeInd: corner for corner in SAFE_EDGES for edgeInd in SAFE_EDGES[corner]}
CORNERS = {0, 7, 56, 63}
CX = {1: 0, 8: 0, 9: 0, 6: 7, 14: 7, 15: 7, 48: 56, 49: 56, 57: 56, 54: 63, 55: 63, 62: 63}
nextMoveCache = {}
makeFlipsCache = {}
visitedBoards = {}

idxs = [i for i in range(0, len(startboard))]
for index in idxs:
    if index % 8 == 0:
        nbrFlips[index] = {index + 1, index - 8, index + 8, index - 7, index + 9}.intersection(idxs) 
    elif index % 8 == 7:
        nbrFlips[index] = {index - 1, index - 8, index + 8, index + 7, index - 9}.intersection(idxs)
    else:
        nbrFlips[index] = {index - 1,index + 1, index - 8, index + 8, index - 7, index + 7, index - 9, index + 9}.intersection(idxs)

for index in idxs:
    subDict = {nbr: [] for nbr in nbrFlips[index]}
    for nbr in nbrFlips[index]:
        diff = index - nbr
        prev = nbr
        current = nbr + diff
        while -1 < current < 64 and current in nbrFlips[prev]:
            if current != index:
                subDict[nbr].append(current)
            prev = current
            current = current + diff
        if len(subDict[nbr]) == 0:
            del subDict[nbr]
    SUBSETS.append(subDict)

nbrMoves = {index: {key for key in SUBSETS[index]} for index in nbrFlips}
delInds = {key for key in nbrMoves if len(nbrMoves[key]) == 0}
for key in delInds:
    del nbrMoves[key]

def oppositeToken(tkn):
    if tkn == 'x':
        return 'o'
    return 'x'

def indexWorks(tkn, possInd, adjInd, board):
    subset = SUBSETS[adjInd][possInd]

    for index in subset:
        if board[index] == '.':
            return -1
        elif board[index] == tkn:
            return index
    return -1

def nextMoves(board, token):
    global nextMoveCache
    if board + token in nextMoveCache:
        return nextMoveCache[board + token]

    possMoves = {}
    oppToken = oppositeToken(token)
    tknSet = {idx for idx in range(64) if board[idx] == oppToken} - {0, 7, 56, 63}

    for idx in tknSet:
        for nbr in nbrMoves[idx]:
            if board[nbr] == '.':
                bracket = indexWorks(token, nbr, idx, board)
                if bracket != -1:
                    subset = SUBSETS[idx][nbr]
                    changes = set(subset[:subset.index(bracket) + 1] + [nbr, idx])
                    if nbr in possMoves:
                        possMoves[nbr] = possMoves[nbr].union(changes)
                    else:
                        possMoves[nbr] = changes
    nextMoveCache[board + token] = possMoves
    return possMoves

def sortMoves(token, oppTkn, board, possMoves):

    sortedMoves = []
    for move in possMoves:
        score = 0

        oppPossMoves = nextMoves(startboard, startTkn)
        if not len(oppPossMoves):
            score += 2

        if move in CORNERS:
            score += 3
        elif move in EDGE_CNR:
            if board[EDGE_CNR[move]] == token:
                score += 1
        if move in CX:
            if board[CX[move]] == '.':
                score = -100
            elif board[CX[move]] == oppTkn:
                score = -99

        sortedMoves.append((score, move))

    return sorted(sortedMoves)

def placePiece(board, token, position, changes):
    global makeFlipsCache
    if board + token + position in makeFlipsCache:
        return makeFlipsCache[board + token + position]
    flippedboard =  ''.join([ch if ind not in changes else token for ind, ch in enumerate(board)])
    makeFlipsCache[board + token + position] = flippedboard
    return flippedboard

def quickMove(board, token):
    movesLeft = board.count('.')
    if movesLeft <= 10:
        nm = negamax(board, token)
        print('Score: {} Sequence: {}'.format(nm[0], nm[1:]))
    else:
        possMoves = nextMoves(board, token)
        possibles = sortMoves(token, oppositeToken(token), board, possMoves)
        print([possible[1] for possible in possibles])

COUNT = 0

def negamax(board, token):

    oppTkn = oppositeToken(token)
    possMoves = nextMoves(board, token)

    if (board, token) in visitedBoards:
        print(visitedBoards[(board, token)])
    
    if not possMoves:
        possOppMoves = nextMoves(board, oppTkn)

        if not possOppMoves:
            score = [board.count(token) - board.count(oppTkn)]
            visitedBoards[(board, oppTkn, {})] = score
            visitedBoards[(board, token, {})] = score
            return score
        
        nm = negamax(board, oppTkn)
        score = [-nm[0]] + nm[1:] + [-1]
        visitedBoards[(board, token, possMoves)] = score
        return score

    best = min(negamax(placePiece(board, token, str(move), possMoves[move]), oppTkn) + [move] for move in possMoves)
    score = [-best[0]] + best[1:]
    visitedBoards[(board, token, possMoves)] = score
    return score

def main():
    quickMove(startboard, startTkn)

                
if __name__ == '__main__':
    main()

#Medha Pappula, 6, 2026