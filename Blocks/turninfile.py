import sys; args = sys.argv[1:]

defaultBoard = '.'*27 + "ox......xo" + '.'*27
NBRS = {}
SUBSETS = []
startboard = defaultBoard
startTkns = ''

inpt = args
inpts = len(inpt)
if inpts == 2:
    if len(inpt[0]) == 64:
        startboard = inpt[0].lower()
        startTkns = inpt[1].lower()
    elif len(inpt[0]) == 1:
        startTkns = inpt[0]
        startboard = inpt[1].lower()
elif inpts == 1:
    if len(inpt[0]) == 64:
        startboard = inpt[0].lower()
    elif len(inpt[0]) == 1:
        startTkns = inpt[0].lower()

idxs = [i for i in range(0, len(defaultBoard))]
for index in idxs:
    if index % 8 == 0:
        NBRS[index] = {index + 1,
                             index - 8, index + 8,
                             index - 7,
                             index + 9}\
            .intersection(idxs)
    elif index % 8 == 7:
        NBRS[index] = {index - 1,
                             index - 8, index + 8,
                             index + 7,
                             index - 9} \
            .intersection(idxs)
    else:
        NBRS[index] = {index - 1,index + 1,
                             index - 8, index + 8,
                             index - 7, index + 7,
                             index - 9, index + 9} \
            .intersection(idxs)

for index in idxs:
    subDict = {nbr: [] for nbr in NBRS[index]}
    for nbr in NBRS[index]:
        diff = index - nbr
        prev = nbr
        current = nbr + diff
        while -1 < current < 64 and current in NBRS[prev]:
            if current != index:
                subDict[nbr].append(current)
            prev = current
            current = current + diff
        if len(subDict[nbr]) == 0:
            del subDict[nbr]
    SUBSETS.append(subDict)

NBRS = {index: {key for key in SUBSETS[index]} for index in NBRS}
delInds = {key for key in NBRS if len(NBRS[key]) == 0}
for key in delInds:
    del NBRS[key]

print(NBRS)
print(SUBSETS)

def printBoard(board):
    for i in range(0, 64, 8):
        print(' '.join(board[i:i+8]))


def printPossMoves(board, possMoves):
    printBoard(''.join([ch if idx not in possMoves
                        else '*' for idx, ch in enumerate(board)]))

def nextTokens(board):
    if board.count('.') % 2:
        return 'o', 'x'
    return 'x', 'o'


def getOppToken(token):
    if token == 'x':
        return 'o'
    return 'x'


def checkBracketing(token, possInd, adjInd, board):

    subset = SUBSETS[adjInd][possInd]

    for index in subset:
        if board[index] == '.':
            return False
        elif board[index] == token:
            return True
    return False



def nextMoves(board, tokens = ''):
    possMoves = set()

    if tokens == '':
        token, oppToken = nextTokens(board)
    else:
        token, oppToken = tokens, getOppToken(tokens)


    for idx in NBRS:
        if board[idx] == oppToken:
            for nbr in NBRS[idx]:
                if board[nbr] == '.':
                    if checkBracketing(token, nbr, idx, board):
                        possMoves.add(nbr)
    return len(possMoves), possMoves


if startTkns != "" and nextTokens(startboard)[0] != startTkns:
    print('No moves possible')
else:
    canMove, possMoves = nextMoves(startboard, startTkns)

    if canMove:
        print(possMoves)
    else:
        print('No moves possible')
        

# Medha Pappula, 6, 2026