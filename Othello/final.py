import sys; args = sys.argv[1:]

startboard = '.'*27 + 'ox......xo' + '.'*27
startTkn = ""
oppTkn = ""
givenMoves = []
nbrFlips = {}
nbrMoves = {}
SUBSETS = []
TKNSETS = {}
SAFE_EDGES = {0: {1,2,3,4,5,6,7,8,16,24,32,40,48,56}, 7: {0,1,2,3,4,5,6,15,23,31,39,47,55,63},
     56: {0,8,16,24,32,40,48,57,58,59,60,61,62,63}, 63: {7,15,23,31,39,47,55,56,57,58,59,60,61,62}}
EDGE_CNR = {edgeInd: corner for corner in SAFE_EDGES for edgeInd in SAFE_EDGES[corner]}
CORNERS = {0, 7, 56, 63}
CX = {1: 0, 8: 0, 9: 0, 6: 7, 14: 7, 15: 7, 48: 56, 49: 56, 57: 56, 54: 63, 55: 63, 62: 63}

def setup(args):
    global startboard, startTkn, givenMoves, nbrFlips, nbrMoves, SUBSETS, TKNSETS, SAFE_EDGES, EDGE_CNR, CORNERS, CX, oppTkn, oppTkn

    for k in range(len(args)):
        if len(args[k]) == 64 and "." in args[k]:
            startboard = args[k].lower()
        elif len(args[k]) in (1, 2):
            if args[k][0] == "-":
                continue
            if args[k].lower() in 'xo':
                startTkn = args[k].lower()
            elif args[k][0].lower() in 'abcdefgh':
                givenMoves.append((int(args[k][1])-1)*8 + 'abcdefgh'.index(args[k][0].lower()))
            else:
                givenMoves.append(int(args[k]))
        else:
            for x in [args[k][i:i+2] for i in range(0, len(args[k]), 2)]:
                if "-" in x:
                    continue
                else:
                    givenMoves.append(int(x.replace("_", "")))

    TKNSETS = {'o': {i for i in range(64) if startboard[i] == 'o'} - {0, 7, 56, 63}, 'x': {i for i in range(64) if startboard[i] == 'x'} - {0, 7, 56, 63}}

    if startTkn == '':
        startTkn, oppTkn = nextTokens(startboard)
    else:
        oppTkn = oppositeToken(startTkn)

    idxs = [i for i in range(0, len(startboard))]

    for index in idxs:
        if index % 8 == 0:
            nbrFlips[index] = {index - 8, index - 7, index + 8, index + 1, index + 9}.intersection(idxs)
        elif index % 8 == 7:
            nbrFlips[index] = {index - 1, index - 8, index - 9, index + 8, index + 7}.intersection(idxs)
        else:
            nbrFlips[index] = {index - 1, index - 8, index - 7, index - 9, index + 1, index + 8, index + 7, index + 9}.intersection(idxs)

    for index in idxs:
        sDict = {nbr: [] for nbr in nbrFlips[index]}
        for nbr in nbrFlips[index]:
            d = index - nbr
            p = nbr
            c = nbr + d
            while -1 < c < 64 and c in nbrFlips[p]:
                if c != index:
                    sDict[nbr].append(c)
                p = c
                c = c + d
            if len(sDict[nbr]) == 0:
               del sDict[nbr]
        SUBSETS.append(sDict)

    nbrMoves = {index: k for index in nbrFlips if len(k:={key for key in SUBSETS[index]}) != 0}

def nextTokens(board):
    if board.count('.') % 2:
        return 'o', 'x'
    return 'x', 'o'

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

def nextMoves(board, tkn = ''):
    global startboard, startTkn, givenMoves, nbrFlips, nbrMoves, SUBSETS, TKNSETS, SAFE_EDGES, EDGE_CNR, CORNERS, CX, oppTkn
    possMoves = set()

    if tkn == '':
        token, oppToken = nextTokens(board)
    else:
        token, oppToken = tkn, oppositeToken(tkn)

    for idx in TKNSETS[oppToken]:
        for nbr in nbrMoves[idx]:
            if board[nbr] == '.':
                if indexWorks(token, nbr, idx, board) != -1:
                    possMoves.add(nbr)
    return possMoves

def choose_move(board, player, still_running, time_limit):
    #setup([board, player])
    #possMoves = nextMoves(board, player)
    #return possMoves[0]

    return board.index(".")


class Strategy:

    def best_strategy(self, board, player, best_move, still_running, time_limit):
        move = choose_move(board, player, still_running, time_limit)
        best_move.value = move