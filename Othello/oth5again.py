import sys; args = sys.argv[1:]

startboard = args[0].lower() if len(args) > 0 else '.'*27 + 'ox......xo' + '.'*27
startTkn = args[1].lower() if len(args) > 1 else {0:'x', 1:'o'}[startboard.count('.')%2]

nbrFlips = {}
nbrMoves = {}
SUBSETS = []
CNR_EDGES = {0: {1,2,3,4,5,6,7,8,16,24,32,40,48,56},
             7: {0,1,2,3,4,5,6,15,23,31,39,47,55,63},
             56: {0,8,16,24,32,40,48,57,58,59,60,61,62,63},
             63: {7,15,23,31,39,47,55,56,57,58,59,60,61,62}}
EDGE_CNR = {edgeInd: corner for corner in CNR_EDGES for edgeInd in CNR_EDGES[corner]}
CORNERS = {0, 7, 56, 63}
CX = {1: 0, 8: 0, 9: 0, 6: 7, 14: 7, 15: 7, 48: 56, 49: 56, 57: 56, 54: 63, 55: 63, 62: 63}
oppTkns = {'x':'o', 'o':'x'}
nextMoveCache = {}
makeFlipsCache = {}

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

def printBoard(board):
    for i in range(0, 64, 8):
        print(' '.join(board[i:i+8]))


def printPossMoves(board, possMoves):
    printBoard(''.join([ch if idx not in possMoves
                        else '*' for idx, ch in enumerate(board)]))


def indexWorks(token, possInd, adjInd, board):

    subset = SUBSETS[adjInd][possInd]

    for index in subset:
        if board[index] == '.':
            # if you run into an empty space before bracketing token
            # then it doesn't work
            return -1
        elif board[index] == token:
            # if you find a bracketing token somewhere along the line
            # then it does form a bracket
            return index # return the ending index
    # if you get through the entire subset and don't find a bracketing token
    # then too bad
    return -1


def nextMoves(board, token): # return moves to be flipped later
    global nextMoveCache
    if board + token in nextMoveCache:
        return nextMoveCache[board + token]

    possMoves = {} # {possible move indexes: indexes they flip}
    oppToken = oppTkns[token]
    tknSet = {idx for idx in range(64) if board[idx] == oppToken} - {0, 7, 56, 63}

    for idx in tknSet: # check opposing token indexes (maybe improve later)
        for nbr in nbrMoves[idx]: # check if there are spaces you can move into
            if board[nbr] == '.':
                bracket = indexWorks(token, nbr, idx, board)
                if bracket != -1:
                    # if placing here check whether there's another
                    # token down the line it would form a bracket with
                    subset = SUBSETS[idx][nbr]
                    changes = set(subset[:subset.index(bracket) + 1] + [nbr, idx])
                    if nbr in possMoves:
                        possMoves[nbr] = possMoves[nbr].union(changes)
                    else:
                        possMoves[nbr] = changes
    nextMoveCache[board + token] = possMoves
    return possMoves


def makeFlips(board, token, move, changes):
    global makeFlipsCache
    if board + token + move in makeFlipsCache:
        return makeFlipsCache[board + token + move]
    # replace all the indexes that should be flipped with your token
    flippedboard =  ''.join([ch if ind not in changes else token for ind, ch in enumerate(board)])
    makeFlipsCache[board + token + move] = flippedboard
    return flippedboard


def estimateMoves(board, token):

    oppTkn = oppTkns[token]
    possMoves = nextMoves(board, token)
    sortedMoves = []

    for move in possMoves:
        score = 0

        oppPossMoves = nextMoves(startboard, startTkn)
        if not oppPossMoves:
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

    return [move for score, move in sorted(sortedMoves)]


def negamax(board, token): # want to return: min guaranteed score, rev. sequence
    oppTkn = oppTkns[token]

    # number of possible moves, set of possible moves
    possMoves = nextMoves(board, token)

    if not possMoves:
        # number of enemy possible moves, set of those moves
        possOppMoves = nextMoves(board, oppTkn)

        if not possOppMoves: # if neither side can move, return final score
            score = [board.count(token) - board.count(oppTkn)]
            #print('POSS SCORE', score)
            return score

        # otherwise, if you get skipped, just negamax from the opponent's side
        nm = negamax(board, oppTkn)
        return [-nm[0]] + nm[1:] + [-1]

    # of the possible scores you might get, find the smallest
    best = min(negamax(makeFlips(board, token, str(move), possMoves[move]), oppTkn)
               + [move] for move in possMoves)
    return [-best[0]] + best[1:]


def printSorted(board, token):
    #print('Board: {}'.format(board))
    movesLeft = board.count('.')
    #print('Moves left: {}'.format(movesLeft))
    if movesLeft <= 10:
        nm = negamax(board, token)
        print('Score: {} Sequence: {}'.format(nm[0], nm[1:]))
    else:
        print('est')
        print(estimateMoves(board, token))


print(estimateMoves(startboard, startTkn))
printSorted(startboard, startTkn)

#Medha Pappula, 6, 2026