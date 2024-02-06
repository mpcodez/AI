import sys; args = sys.argv[1:]

args = ["v"]

startboard = '.'*27 + 'ox......xo' + '.'*27
startTkn = {0:'x', 1:'o'}[startboard.count('.')%2]
moveList = []
visitedBoards = {}
verbose = False
kickin = 12

for k in range(len(args)):
    if len(args[k]) == 64:
        startboard = args[k].lower()
    elif len(args[k]) in (1, 2):
        if args[k][0] == "-":
            continue
        if args[k].lower() in 'xo':
            startTkn = args[k].lower()
        elif args[k][0].lower() in 'abcdefgh':
            moveList.append((int(args[k][1])-1)*8 + 'abcdefgh'.index(args[k][0].lower()))
        elif args[k].lower() == "v":
            verbose = True
        else:
            moveList.append(int(args[k]))
    else:
        if "HL" not in args[k]:
            for x in [args[k][i:i+2] for i in range(0, len(args[k]), 2)]:
                if "-" in x:
                    continue
                else:
                    moveList.append(int(x.replace("_", "")))
        else:
            kickin = int(args[k].replace("HL", ""))

NBRS_flips = {}
NBRS_moves = {}
NBRS_moves_r = {}
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
        NBRS_flips[index] = {index + 1, index - 8, index + 8, index - 7, index + 9}.intersection(idxs)
    elif index % 8 == 7:
        NBRS_flips[index] = {index - 1, index - 8, index + 8, index + 7, index - 9}.intersection(idxs)
    else:
        NBRS_flips[index] = {index - 1,index + 1, index - 8, index + 8, index - 7, index + 7, index - 9, index + 9}.intersection(idxs)

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

NBRS_moves = {index: {key for key in SUBSETS[index]} for index in NBRS_flips}
delInds = {key for key in NBRS_moves if len(NBRS_moves[key]) == 0}
for key in delInds:
    del NBRS_moves[key]
NBRS_moves_r = {index: {key for key in NBRS_moves if index in NBRS_moves[key]} for index in range(64)}

def setup(args):
    global startboard, startTkn, SUBSETS, EDGE_CNR, CORNERS, CX, visitedBoards, oppTkns, makeFlipsCache, nextMoveCache, NBRS_moves_r
    startboard = '.'*27 + 'ox......xo' + '.'*27
    startTkn = {0:'x', 1:'o'}[startboard.count('.')%2]
    moveList = []
    visitedBoards = {}

    for k in range(len(args)):
        if len(args[k]) == 64:
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

    NBRS_flips = {} # NBRS_flips = {index: {adjacent indexes}}
    NBRS_moves = {} # NBRS_moves = {index: {adjacent indexes that moves can be made from}}
    NBRS_moves_r = {} # reverse for checking from space
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

    idxs = [i for i in range(0, len(startboard))]
    for index in idxs:
        if index % 8 == 0:
            NBRS_flips[index] = {index + 1, index - 8, index + 8, index - 7, index + 9}.intersection(idxs)
        elif index % 8 == 7:
            NBRS_flips[index] = {index - 1, index - 8, index + 8, index + 7, index - 9}.intersection(idxs)
        else:
            NBRS_flips[index] = {index - 1,index + 1, index - 8, index + 8, index - 7, index + 7, index - 9, index + 9}.intersection(idxs)

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

    NBRS_moves = {index: {key for key in SUBSETS[index]} for index in NBRS_flips}
    delInds = {key for key in NBRS_moves if len(NBRS_moves[key]) == 0}
    for key in delInds:
        del NBRS_moves[key]
    NBRS_moves_r = {index: {key for key in NBRS_moves if index in NBRS_moves[key]} for index in range(64)}

def printBoard(board):
    for i in range(0, 64, 8):
        print(' '.join(board[i:i+8]))


def printPossMoves(board, possMoves):
    printBoard(''.join([ch if idx not in possMoves else '*' for idx, ch in enumerate(board)]))


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


def makeFlips(board, token, move, possMoves):
    global makeFlipsCache
    changes = possMoves[move]
    move = str(move)
    if board + token + move in makeFlipsCache:
        return makeFlipsCache[board + token + move]
    flippedboard =  ''.join([ch if ind not in changes else token for ind, ch in enumerate(board)])
    makeFlipsCache[board + token + move] = flippedboard
    return flippedboard

def placePiece(board, token, move, changes):
    global makeFlipsCache
    if board + token + move in makeFlipsCache:
        return makeFlipsCache[board + token + move]
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

def moveIt(board, token):

    movesLeft = board.count('.')
    if movesLeft <= kickin:
        ab = alphabeta(board, token, -65, 65)
        print('Score: {} Sequence: {}'.format(ab[0], ab[1:]))
    else:
        possibles = estimateMoves(board, token)
        return possibles[len(possibles)-1]

def quickMove(board, token):
    setup([board, token])
    oppTkn = getOppToken(token)
    possibles = estimateMoves(board, token)
    return possibles[len(possibles)-1]

def play(tkn, oppTkn, movePos, board):
    if verbose:
        print('\n{} plays to {}'.format(tkn, movePos))
    possMoves = nextMoves(board, tkn)
    flippedBoard = makeFlips(board, tkn, movePos, possMoves)
    possOppMoves = nextMoves(flippedBoard, oppTkn)
    xTokens, oTokens = getScore(flippedBoard)
    if len(possOppMoves) != 0:
        if verbose:
            printPossMoves(flippedBoard[:movePos] + tkn.upper() + flippedBoard[movePos+1:], possOppMoves)
            print(flippedBoard[:movePos] + tkn.upper() + flippedBoard[movePos+1:] + ' {}/{}'.format(xTokens, oTokens))
            print('Possible moves for {}: {}'.format(oppTkn, list(possOppMoves.keys())))
        return oppTkn, tkn, flippedBoard
    else:
        if verbose:
            printPossMoves(flippedBoard[:movePos] + tkn.upper() + flippedBoard[movePos+1:], possOppMoves)
            print(flippedBoard[:movePos] + tkn.upper() + flippedBoard[movePos+1:] + ' {}/{}'.format(xTokens, oTokens))
            print("No Moves Possible")
        possMoves = nextMoves(flippedBoard, tkn)
        if len(possMoves) != 0:
            if verbose:
                printPossMoves(flippedBoard[:movePos] + tkn.upper() + flippedBoard[movePos+1:], possOppMoves)
                print(flippedBoard[:movePos] + tkn.upper() + flippedBoard[movePos+1:] + ' {}/{}'.format(xTokens, oTokens))
                print('Possible moves for {}: {}'.format(tkn, list(possMoves.keys())))
        else:
            if verbose:
                printPossMoves(flippedBoard[:movePos] + tkn.upper() + flippedBoard[movePos+1:], possOppMoves)
                print(flippedBoard[:movePos] + tkn.upper() + flippedBoard[movePos+1:] + ' {}/{}'.format(xTokens, oTokens))
                print("No Moves Possible")
        return tkn, oppTkn, flippedBoard

def getScore(board):
    return board.count('x'), board.count('o')


def nextTokens(board):
    if board.count('.') % 2:
        return 'o', 'x'
    return 'x', 'o'

def getOppToken(token):
    if token == 'x':
        return 'o'
    return 'x'

def negamax(board, token):
    oppTkn = oppTkns[token]

    possMoves = nextMoves(board, token)

    if not possMoves:
        possOppMoves = nextMoves(board, oppTkn)

        if not possOppMoves:
            score = [board.count(token) - board.count(oppTkn)]
            return score

        nm = negamax(board, oppTkn)
        return [-nm[0]] + nm[1:] + [-1]

    best = min(negamax(placePiece(board, token, str(move), possMoves[move]), oppTkn)
               + [move] for move in possMoves)
    return [-best[0]] + best[1:]


def printSorted(board, token):
    movesLeft = board.count('.')
    if movesLeft <= 10:
        nm = negamax(board, token)
        print('Score: {} Sequence: {}'.format(nm[0], nm[1:]))
    else:
        print(estimateMoves(board, token))


def alphabeta(board, token, lower, upper): # want to return: min guaranteed score, rev. sequence
    oppTkn = oppTkns[token]

    possMoves = nextMoves(board, token)

    if not possMoves:
        possOppMoves = nextMoves(board, oppTkn)

        if not possOppMoves:
            score = [board.count(token) - board.count(oppTkn)]
            return score

        ab = alphabeta(board, oppTkn, -upper, -lower)
        return [-ab[0]] + ab[1:] + [-1]

    best = [lower - 1]
    for move in possMoves:
        ab = alphabeta(makeFlips(board, token, move, possMoves), oppTkn, -upper, -lower)
        score = -ab[0]
        if score > upper:
            return [score]
        if score < lower:
            continue
        best = [score] + ab[1:] + [move]
        lower = score + 1
    return best


def alphabetaTopLvl(board, token, lower, upper): # want to return: min guaranteed score, rev. sequence
    oppTkn = oppTkns[token]

    possMoves = nextMoves(board, token)

    if not possMoves:
        possOppMoves = nextMoves(board, oppTkn)

        if not possOppMoves:
            score = [board.count(token) - board.count(oppTkn)]
            return score

        ab = alphabeta(board, oppTkn, -upper, -lower)
        return [-ab[0]] + ab[1:] + [-1]

    best = [lower - 1]
    for move in possMoves:
        ab = alphabeta(makeFlips(board, token, move, possMoves), oppTkn, -upper, -lower)
        score = -ab[0]
        if score > upper:
            return [score]
        if score < lower:
            continue
        best = [score] + ab[1:] + [move]
        lower = score + 1

    return best


def main():
    global startTkn, startboard

    if args != [] and "HL" in args[len(args)-1]:
        moveIt(startboard, startTkn)
    else:
        startTkn, oppTkn = nextTokens(startboard)

        possMoves = nextMoves(startboard, startTkn)
        if len(possMoves) == 0:
            possMoves = nextMoves(startboard, oppTkn)
            startTkn, oppTkn = oppTkn, startTkn
        
        if len(moveList) == 0:
            if len(possMoves) != 0:
                printPossMoves(startboard, possMoves)
                xTokns, oTokns = getScore(startboard)
                print('\n' + startboard + ' {}/{}'.format(xTokns, oTokns)) 
                print('Possible moves for {}: {}'.format(startTkn, list(possMoves.keys())))
                print()
                print("My preferred move is: " + str(quickMove(startboard, startTkn)))
                if kickin != 0 and startboard.count(".") <= kickin:
                    moveIt(startboard, startTkn)

        else:

            possMoves = nextMoves(startboard, startTkn)

            if len(possMoves) != 0:
                printPossMoves(startboard, possMoves)
                print()
                xTokns, oTokns = getScore(startboard)
                print(startboard + ' {}/{}'.format(xTokns, oTokns)) 
                print('Possible moves for {}: {}'.format(startTkn, list(possMoves.keys())))
                if kickin != 0 and startboard.count(".") <= kickin:
                    moveIt(startboard, startTkn)
                
            for movePos in moveList:
                if movePos < 0:
                    continue
                mP = movePos
                if movePos in nextMoves(startboard, startTkn):
                    s = startTkn
                    startTkn, oppTkn, startboard = play(startTkn, oppTkn, movePos, startboard)   
                elif movePos in nextMoves(startboard, oppTkn):
                    s = oppTkn
                    startTkn, oppTkn, startboard = play(oppTkn, startTkn, movePos, startboard)
            
            print('\n{} plays to {}'.format(s, mP))
            
            print()
            movePos = moveList[len(moveList)-1]
            possOppMoves = [key for key in nextMoves(startboard, startTkn)]
            printPossMoves(startboard[:movePos] + startboard[movePos].upper() + startboard[movePos+1:], possOppMoves)
            xTokens, oTokens = getScore(startboard)
            print(startboard[:movePos] + startboard[movePos].upper() + startboard[movePos+1:] + ' {}/{}'.format(xTokens, oTokens))
            if len(possOppMoves) != 0:
                print('Possible moves for {}: {}'.format(startTkn, str(possOppMoves).replace("[", "").replace("]", "")))
                print("My preferred move is: " + str(quickMove(startboard, startTkn)))
            else:
                print("No Moves Possible")


if __name__ == '__main__':
    main()

#Medha Pappula, 6, 2026