import sys; args = sys.argv[1:]

startboard = '.'*27 + 'ox......xo' + '.'*27
startTkn = ""
moveList = []
args = []

for k in range(len(args)):
    if len(args[k]) == 64 and "." in args[k]:
        startboard = args[k].lower()
    elif len(args[k]) in (1, 2):
        if args[k][0] == "-":
            continue
        if args[k].lower() in 'xo':
            startTkn = args[k].lower()
        elif args[k][0].lower() in 'abcdefgh':
            moveList.append((int(args[k][1])-1)*8 + 'abcdefgh'.index(args[k][0].lower()))
        else:
            moveList.append(int(args[k]))
    else:
        for x in [args[k][i:i+2] for i in range(0, len(args[k]), 2)]:
            if "-" in x:
                continue
            else:
                moveList.append(int(x.replace("_", "")))

# global variables
OPPS = {'x': 'o', 'o': 'x'}
NBRS_flips = {} # NBRS_flips = {index: {adjacent indexes}}
NBRS_moves = {} # NBRS_moves = {index: {adjacent indexes that moves can be made from}}
SUBSETS = [] # SUBSETS = [{nbr: [indexes in subset], nbr: [indexes in subset]}, {etc...}]
TKNSETS = {'o': {i for i in range(64) if startboard[i] == 'o'} - {0, 7, 56, 63},
             'x': {i for i in range(64) if startboard[i] == 'x'} - {0, 7, 56, 63}} # set of indexes containing o and x
CNR_EDGES = {0: {1,2,3,4,5,6,7,8,16,24,32,40,48,56}, 7: {0,1,2,3,4,5,6,15,23,31,39,47,55,63},
         56: {0,8,16,24,32,40,48,57,58,59,60,61,62,63}, 63: {7,15,23,31,39,47,55,56,57,58,59,60,61,62}}
EDGE_CNR = {edgeInd: corner for corner in CNR_EDGES for edgeInd in CNR_EDGES[corner]}
CORNERS = {0, 7, 56, 63}
CX = {1: 0, 8: 0, 9: 0, 6: 7, 14: 7, 15: 7, 48: 56, 49: 56, 57: 56, 54: 63, 55: 63, 62: 63}



# setting up NBRS -- part 1
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


# setting up SUBSETS
for index in idxs: # want a dict for each index
    subDict = {nbr: [] for nbr in NBRS_flips[index]}
    for nbr in NBRS_flips[index]: # want a key for each neighbor
        # want the value to be a list of the other indexes in the same
        # row/column/diagonal, depending on the relationship between the
        # index and neighbor (which determines whether you're looking at
        # diagonals, columns, or rows)
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


# taking out NBRS that moves can't be made from
NBRS_moves = {index: {key for key in SUBSETS[index]} for index in NBRS_flips}
delInds = {key for key in NBRS_moves if len(NBRS_moves[key]) == 0}
for key in delInds:
    del NBRS_moves[key]


# helper methods
def getScore(board):
    return board.count('x'), board.count('o')


def nextTokens(board): # assuming no passes
    if board.count('.') % 2: # do better later
        return 'o', 'x' # next token, token after
    return 'x', 'o'


def getOppToken(token):
    if token == 'x':
        return 'o'
    return 'x'


def printBoard(board):
    for i in range(0, 64, 8):
        print(' '.join(board[i:i+8]))


def printPossMoves(board, possMoves):
    printBoard(''.join([ch if idx not in possMoves
                        else '*' for idx, ch in enumerate(board)]))


def checkBracketing(token, possInd, adjInd, board):
    # your token, possible placement index, adjacent index of opponent, current board
    # return true or false depending on whether your token would
    # form a bracket with a matching token if placed next to index
    # also try to think of better ways to go about this

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


def nextMoves(board, tokens = ''):
    possMoves = set() # {indexes that given/default token may make a move at}

    if tokens == '': # if token isn't given
        token, oppToken = nextTokens(board) # assume no passes and find next token
    else:
        token, oppToken = tokens, getOppToken(tokens)

    for idx in TKNSETS[oppToken]:
        for nbr in NBRS_moves[idx]:
            if board[nbr] == '.':
                if checkBracketing(token, nbr, idx, board) != -1:
                    possMoves.add(nbr)
    return len(possMoves), possMoves


def makeFlips(board, token, position):
    oppToken = getOppToken(token)

    adjOpps = {nbr for nbr in NBRS_flips[position]
               if board[nbr] == oppToken and position in SUBSETS[nbr]}

    for opp in adjOpps: # do better later
        idx = checkBracketing(token, position, opp, board) # maybe pass in idx rather than re-finding
        if idx > -1:
            subset = SUBSETS[opp][position]
            changes = set(subset[:subset.index(idx) + 1] + [position, opp])
            TKNSETS[token] = TKNSETS[token].union(changes) - {0, 7, 56, 63}
            TKNSETS[oppToken] = TKNSETS[oppToken] - changes
            board = ''.join([ch if ind not in changes else token for ind, ch in enumerate(board)])
    return board


def sortMoves(token, oppTkn, board, possMoves):
    sortedMoves = []
    for move in possMoves:
        score = 0

        oppCanMove, oppPossMoves = nextMoves(startboard, startTkn)
        if not oppCanMove:
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


def quickMove(board, token):
    oppTkn = getOppToken(token)
    canMove, possMoves = nextMoves(board, token)
    possibles = sortMoves(token, oppTkn, board, possMoves)
    return possibles[len(possibles)-1][1]

def play(tkn, oppTkn, movePos, board):
    print('\nPlayer {} moves to {}:'.format(tkn, movePos))
    flippedBoard = makeFlips(board, tkn, movePos)
    canOppMove, possOppMoves = nextMoves(flippedBoard, oppTkn)
    printBoard(flippedBoard)
    xTokens, oTokens = getScore(flippedBoard)
    print('\n' + flippedBoard + ' {}/{}'.format(xTokens, oTokens))
    if canOppMove:
        print('Possible moves for {}: {}'.format(oppTkn, possOppMoves))
        return oppTkn, tkn, flippedBoard
    else:
        canMove, possMoves = nextMoves(flippedBoard, tkn)
        if canMove:
            print('Possible moves for {}: {}'.format(tkn, possMoves))
        return tkn, oppTkn, flippedBoard

if startTkn == '':
    startTkn, oppTkn = nextTokens(startboard)
else:
    oppTkn = getOppToken(startTkn)

canMove, possMoves = nextMoves(startboard, startTkn)
if canMove == False:
    canMove, possMoves = nextMoves(startboard, oppTkn)
    startTkn, oppTkn = oppTkn, startTkn

if len(moveList) == 0:
    xTokens, oTokens = getScore(startboard)
    printBoard(startboard)
    print('\n' + startboard + ' {}/{}'.format(xTokens, oTokens))
    if canMove:
        print('Possible moves for {}: {}'.format(startTkn, possMoves))

else:
    xTokens, oTokens = getScore(startboard)
    canMove, possMoves = nextMoves(startboard, startTkn)
    printBoard(startboard)
    print('\n' + startboard + ' {}/{}'.format(xTokens, oTokens))
    if canMove:
        print('Possible moves for {}: {}'.format(startTkn, possMoves))
    for movePos in moveList:
        startTkn, oppTkn, startboard = play(startTkn, oppTkn, movePos, startboard)

#run
print()
canMove, possMoves = nextMoves(startboard, startTkn)
if canMove:
    move = quickMove(startboard, startTkn)
    #print(move)
    play(startTkn, oppTkn, move, startboard)

#Medha Pappula, 6, 2026