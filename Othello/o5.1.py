import sys; args = sys.argv[1:]

args = "xxxxxxxxxxxxxoooxxxxoxooxooxxoooxxoxxoooxxxoooooxxxoooooooooox.o o".split(" ")

startboard = args[0].lower() if len(args) > 0 else '.'*27 + 'ox......xo' + '.'*27
startTkn = args[1].lower() if len(args) > 1 else {0:'x', 1:'o'}[startboard.count('.')%2]

# global variables
NBRS_flips = {} # NBRS_flips = {index: {adjacent indexes}}
NBRS_moves = {} # NBRS_moves = {index: {adjacent indexes that moves can be made from}}
SUBSETS = [] # SUBSETS = [{nbr: [indexes in subset], nbr: [indexes in subset]}, {etc...}]
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

# setting up NBRS
idxs = [i for i in range(0, len(startboard))]
for index in idxs: # make better later if time/energy/if its worth it
    if index % 8 == 0: # if its on left edge, don't include anything left
        NBRS_flips[index] = {index + 1,
                             index - 8, index + 8,
                             index - 7,
                             index + 9}\
            .intersection(idxs) # don't include indexes that don't exist
    elif index % 8 == 7: # if its on right edge, don't include anything right
        NBRS_flips[index] = {index - 1,
                             index - 8, index + 8,
                             index + 7,
                             index - 9} \
            .intersection(idxs)
    else:
        NBRS_flips[index] = {index - 1,index + 1,
                             index - 8, index + 8,
                             index - 7, index + 7,
                             index - 9, index + 9} \
            .intersection(idxs)

for index in idxs:
    subDict = {nbr: [] for nbr in NBRS_flips[index]}
    for nbr in NBRS_flips[index]:
        diff = index - nbr
        prev = nbr
        current = nbr + diff
        while -1 < current < 64 and current in NBRS_flips[prev]:
            if current != index:
                subDict[nbr].append(current)
            prev = current
            current = current + diff
        if len(subDict[nbr]) == 0:
            del subDict[nbr]
    SUBSETS.append(subDict)

# taking out neighbors that moves can't be made from
NBRS_moves = {index: {key for key in SUBSETS[index]} for index in NBRS_flips}
delInds = {key for key in NBRS_moves if len(NBRS_moves[key]) == 0}
for key in delInds:
    del NBRS_moves[key]

# helper methods
def printBoard(board):
    for i in range(0, 64, 8):
        print(' '.join(board[i:i+8]))


def printPossMoves(board, possMoves):
    # print board with asterisks in place of possible moves
    printBoard(''.join([ch if idx not in possMoves
                        else '*' for idx, ch in enumerate(board)]))


def checkBracketing(token, possInd, adjInd, board):

    subset = SUBSETS[adjInd][possInd]

    for index in subset:
        if board[index] == '.':
            return -1
        elif board[index] == token:
            return index
    return -1


def nextMoves(board, token):
    global nextMoveCache
    if board + token in nextMoveCache:
        return nextMoveCache[board + token]

    possMoves = {}
    oppToken = oppTkns[token]
    tknSet = {idx for idx in range(64) if board[idx] == oppToken} - {0, 7, 56, 63}

    for idx in tknSet:
        for nbr in NBRS_moves[idx]:
            if board[nbr] == '.':
                bracket = checkBracketing(token, nbr, idx, board)
                if bracket != -1:
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
    flippedboard =  ''.join([ch if ind not in changes else token for ind, ch in enumerate(board)])
    makeFlipsCache[board + token + move] = flippedboard
    return flippedboard


def estimateMoves(board, token):
    # estimate best moves without using recursion
    # could be improved but satisfactory for grade
    # remember that the grader looks at the last int printed, so
    # print the best move last -- ascending order in this case
    oppTkn = oppTkns[token]
    possMoves = nextMoves(board, token)
    sortedMoves = []

    for move in possMoves:
        score = 0

        oppPossMoves = nextMoves(startboard, startTkn)
        if not oppPossMoves:
            score += 2

        # just checking for corners and edges and stuff like that
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
    movesLeft = board.count('.')
    if movesLeft <= 10:
        nm = negamax(board, token)
        print('Score: {} Sequence: {}'.format(nm[0], nm[1:]))
    else:
        print(estimateMoves(board, token))

printSorted(startboard, startTkn)

#Medha Pappula, 6, 2026