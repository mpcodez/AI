import sys; args = sys.argv[1:]

def switchTok(token):
    return 'X' if token == 'O' else 'O'

default = '.'*27 + 'OX......XO' + '.'*27
nbrs = {}
indexList = []
futMoveCache = {}
cbCache = {}
holeLim = 0
movesCache = {}
makerCache = {}
sequenceCache = {}


moveBoard = {index: {key for key in indexList[index]} for index in nbrs}
getRid = {key for key in moveBoard if len(moveBoard[key]) == 0}
for i in getRid:
    del moveBoard[i]
oTok = {'X':'O', 'O':'X'}
CNR_EDGES = {0: {1,2,3,4,5,6,7,8,16,24,32,40,48,56},
             7: {0,1,2,3,4,5,6,15,23,31,39,47,55,63},
             56: {0,8,16,24,32,40,48,57,58,59,60,61,62,63},
             63: {7,15,23,31,39,47,55,56,57,58,59,60,61,62}}
EDGE_CNR = {edgeInd: cnr for cnr in CNR_EDGES for edgeInd in CNR_EDGES[cnr]}

def printBoard(board, possMoves):
    print("\n".join(["".join([board[i] if i not in possMoves else "*" for i in range(ind, ind+8)]) for ind in range(0, len(board), 8)]) + "\n")

n = "0123456789"
TOKS = ".oOXx"
dot = "."

cnr = [0, 7, 56, 63]
cnrS = {0, 7, 56, 63}
cnrNeigh = {1: 0, 8: 0, 9: 0, 6: 7, 14: 7, 15: 7, 48: 56, 49: 56, 57: 56, 54: 63, 55: 63, 62: 63}

top = {i for i in range(8)}
bottom = {(56) + i for i in range(8)}

left = {(8 * i) for i in range(8)}
right = {7 + (8 * i) for i in range(8)}

allEdges = set()
allEdges.update(top, left, right, bottom)

indexes = []
for r in range(0, 8):
    indexes.append([(r * 8) + v for v in range(8)])

for c in range(0, 8):
    indexes.append([c + (8 * n) for n in range(8)])

for j in range(8 - 2):
    indexes.append([(j + i * (8 + 1)) for i in range(8 - j)])

for j in range(8, 64 - 8 * 2, 8):
    indexes.append([(j + i * (8 + 1)) for i in range(8 - (j // 8))])

for j in range(2, 8):
    indexes.append([(j + i * (8 - 1)) for i in range(0, j + 1)])

for j in range(8 * 2 - 1, 64 - 8 * 2, 8):
    indexes.append([(j + i * (8 - 1)) for i in range(8 - (j // 8))])

indConts = {i: [indexSet for indexSet in indexes if i in indexSet] for i in range(0, 64)}

indexToks = {'O': {i for i in range(64) if default[i] == 'O'} - {0, 7, 56, 63}, 'X': {i for i in range(64) if default[i] == 'X'} - {0, 7, 56, 63}}

def main():
    board = ""
    token = ""
    default = '.' * 27 + 'OX......XO' + '.' * 27
    holeLim = 13
    verb = False
    listMoves = []
    for i in range(len(args)):
        if not args[i]:continue
        if args[i].upper() == "V": verb = True
        elif len(args[i]) >= 3 and args[i][:2] == 'HL':
            holeLim = int(args[i][2:])
        elif len(args[i]) == 64 and args[i][0] in TOKS:
            board = args[i].upper()
        elif args[i].upper() in TOKS: token = args[i].upper()
        else:
            listMoves = condensedPath(listMoves, args[i])

    if not board:
        board = default
    if not token:
        token = switch(board)

    dotPos = {i for i in range(64) if board[i] == "."} #change
    moveSet = findMoves(board, token, dotPos)
    if not moveSet:
        token = switchTok(token)
        moveSet = findMoves(board, token, dotPos)
    global startboard, startTok
    startboard = board
    startTok = token
    if not listMoves:
        printBoard(board, moveSet)
        print(board + " " + str(board.count("X")) + "/" + str(board.count("O")))
        print("Possible moves for " + token + ": " + ", ".join([str(ch) for ch in moveSet]) + "\n")

    counter = 0
    for j in range(0, len(listMoves)):
        i = listMoves[j]
        if i >= 0:
            if j == len(listMoves) - 1 or verb:
                print(token + " moves to " + str(i))
            board, dotPos = makeMove(board, token, i, dotPos)
            Ihatethegrader = board[:i] + token.lower() + board[i+1:]


            token = switchTok(token)
            moveSet = findMoves(board, token, dotPos)
            if not moveSet:
                token = switchTok(token)
                moveSet = findMoves(board, token, dotPos)

            if j == len(listMoves)-1 or verb:
                printBoard(Ihatethegrader, moveSet)
                print(Ihatethegrader + " " + str(board.count("X")) + "/" + str(board.count("O")))
                if moveSet:
                    print("Possible moves for " + token + ": " + ", ".join([str(ch) for ch in sorted(moveSet)]) + "\n")
                if not moveSet:
                    print("No Moves Possible")
                    break
            counter += 1

    movesLeft = board.count('.')
    if movesLeft > 0 and len(moveSet) > 0:
        print("Preferred Move: ", movePref(moveSet, board, token, dotPos))
        if movesLeft < holeLim:
            ab = alphabetaMain(board, token, -65, 65, dotPos)
        else:
            if movePref(moveSet, board, token, dotPos) not in cnrS:
                midgame(board, token, -100000, 100000, 1, dotPos)


def condensedPath(listMoves, movePath):
    if len(movePath) == 1:
        listMoves.append(int(movePath))
        return listMoves
    moveList = [movePath[i:i+2] for i in range(0, len(movePath), 2)]
    for play in moveList:
        if play[0] == "_":
            listMoves.append(int(play[1]))
            continue
        if play[0] == "-" or play[0] in n:
            listMoves.append(int(play))
            continue
        if play[0].upper() in 'ABCDEFGH':
            col = 'ABCDEFGH'.index(play[0].upper())
            listMoves.append(col+ (int(play[1])-1)*8)
    return listMoves

def checkFunction(board, token, e1, e2, ind, spacer, mode):
    if mode == 0:
        while ind not in e1:
            if board[ind] == token:
                return True
            if board[ind] == ".":
                return False
            ind += spacer
        if board[ind] == token:
            return True
        return False
    while ind not in e1 and ind not in e2:
        if board[ind] == token:
            return True
        if board[ind] == ".":
            return False
        ind += spacer
    if board[ind] == token:
        return True
    return False

def findMoves(board, token, dP):
    moveSet = set()
    for ind in dP:
        if ind not in bottom:
            if board[ind+8] == opptokens[token]:
                if checkFunction(board, token, bottom, 1, ind+8, 8, 0):
                    moveSet.add(ind)
                    continue
            if ind not in right and board[ind+9] == opptokens[token]: #check
                if checkFunction(board, token, bottom, right, ind + 9, 9, 1):
                    moveSet.add(ind)
                    continue
            if ind not in left and board[ind+7] == opptokens[token]: #check
                if checkFunction(board, token, left, bottom, ind + 7, 7, 1):
                    moveSet.add(ind)
                    continue
        if ind not in top:
            if board[ind-8] == opptokens[token]:
                if checkFunction(board, token, top, 1, ind - 8, -8, 0):
                    moveSet.add(ind)
                    continue
            if ind not in right and board[ind-7] == opptokens[token]: #check
                if checkFunction(board, token, top, right, ind - 7, -7, 1):
                    moveSet.add(ind)
                    continue
            if ind not in left and board[ind-9] == opptokens[token]: #check
                if checkFunction(board, token, left, top, ind - 9, -9, 1):
                    moveSet.add(ind)
                    continue
        if ind not in right and board[ind+1] == opptokens[token]:
            if checkFunction(board, token, right, 1, ind + 1, 1, 0):
                moveSet.add(ind)
                continue
        if ind not in left and board[ind-1] == opptokens[token]:
            if checkFunction(board, token, left, 1, ind - 1, -1, 0):
                moveSet.add(ind)
                continue
    return moveSet

def flipThemBoyz(board, token, indList, switchToks):
    flipSet = set()
    ind = 0
    while board[indList[ind]] != token and board[indList[ind]] != dot:
        flipSet.add(indList[ind])
        ind += 1
        if ind >= len(indList): return switchToks
    if board[indList[ind]] == token:
        switchToks.update(flipSet)
    return switchToks



def setitems(mv, cL):
    place = cL.index(mv)
    return place, cL[:place][::-1], cL[place + 1:]

def flipTokens(board, token, indList, switcher):
    ind = 0
    possibleFlips = set()
    while board[indList[ind]] != token and board[indList[ind]] != ".":
        possibleFlips.add(indList[ind])
        ind += 1
        if ind >= len(indList):
            return switcher
    if board[indList[ind]] == token:
        switcher.update(possibleFlips)
    return switcher

def makeMove(board, token, mv, dP):
    switcher = {mv}
    dotInds = set()
    for i in dP:
        if i != mv:
            dotInds.add(i)
    for lister in indConts[mv]:
        movePlacement = lister.index(mv)
        prevInd = lister[:movePlacement][::-1]
        futInd = lister[movePlacement+1:]
        if futInd and len(futInd) > 1:
            switcher = flipTokens(board, token, futInd, switcher)
        if prevInd and len(prevInd) > 1:
            switcher = flipTokens(board, token, prevInd, switcher)
    return ("".join([board[i] if i not in switcher else token for i in range(64)]), dotInds)


def edgeSearch(spot_1, spot_2, openSpot, edges, move, board, token):
    edgeTok = switchTok(token)
    edgeTokPoss = False
    ind = move + openSpot
    if board[ind] == edgeTok:
        edgeTokPoss = True
    if board[spot_2] == token:
        while ind != spot_2:
            if board[ind] == dot or (board[ind] == edgeTok and not edgeTokPoss):
                break
            if board[ind] == token and edgeTokPoss:
                edgeTokPoss = False
            ind += openSpot
        if ind == spot_2:
            edges.add(move)
    edgeTokPoss = False
    ind = move - openSpot
    if board[ind] == edgeTok: edgeTokPoss = True
    if board[spot_1] == token:
        while ind != spot_1:
            if board[ind] == dot or (board[ind] == edgeTok and not edgeTokPoss):
                break
            if board[ind] == token and edgeTokPoss: edgeTokPoss = False
            ind = ind - openSpot
        if ind == spot_1: edges.add(move)
    return edges

def countToks(board, edge, token):
    counter = 0
    for i in edge:
        if board[i] == token:
            counter +=1
    return counter

def playBall(possMoveSet, board, token, dP):
    failed = []
    passed = []
    edgeTok = switchTok(token)
    for move in possMoveSet:
        b, d = makeMove(board, token, move, dP)
        if any([True for m in findMoves(b, edgeTok, d) if m in cnr]):
            failed.append(move)
        else: passed.append(move)
    if passed: return passed[0]
    return failed[0]

def switch(board):
    if board.count('.') % 2 == 0:
        return 'X'
    return 'O'

def movePref(possMoveSet, board, token, dP):
    possEdge = set()
    edgeSet = set()
    prospects = set()
    for move in possMoveSet:
        if move in cnr:
            return move
    for i in possMoveSet:
        prospects.add(i)

    for i in possMoveSet:
        pick = True
        if i in cnrNeigh:
            if board[cnrNeigh[i]] != token:
                prospects.remove(i)
                pick = False
        if i in allEdges:

            if i in left:
                possEdge = edgeSearch(0, 56, 8, possEdge, i, board, token)
                if countToks(board, left, dot) == 1:
                    possEdge.add(i)

            elif i in top:
                possEdge = edgeSearch(0, 7, 1, possEdge, i, board, token)
                if countToks(board, top, dot) == 1:
                    possEdge.add(i)

            elif i in right:
                possEdge = edgeSearch(7, 63, 8, possEdge, i, board, token)
                if countToks(board, right, dot) == 1:
                    possEdge.add(i)

            elif i in bottom:
                possEdge = edgeSearch(56, 63, 1, possEdge, i, board, token)
                if countToks(board, bottom, dot) == 1:
                    possEdge.add(i)

            if pick: edgeSet.add(i)

    if possEdge:
        keepTrack = {}
        for m in possEdge:
            changedBoard = makeMove(board, token, m, dP)[0]
            if m in top:
                keepTrack[countToks(changedBoard, top, token)] = m
            elif m in bottom:
                keepTrack[countToks(changedBoard, bottom, token)] = m
            elif m in left:
                keepTrack[countToks(changedBoard, left, token)] = m
            else:
                keepTrack[countToks(changedBoard, right, token)] = m
        ind = max(keepTrack)
        return keepTrack[ind]

    if prospects: return playBall(prospects, board, token, dP)
    return playBall(possMoveSet, board, token, dP)

def quickMove(board, token):
    if not board:
        global holeLim
        holeLim = token
    else:
        board = board.upper()
        token = token.upper()
        possMoveSet = findMoves(board, token)
        numHoles = board.count('.')
        if numHoles < holeLim:
            ab = alphabetaMain(board, token, -65, 65)
            return ab[-1]
        return movePref(possMoveSet, board, token)


#Othello7
opptokens = {'X':'O', 'O':'X'}
def alphabeta(board, token, lwrBnd, uprBnd, dP):
    cnrMoves = []
    goingMoves = []
    opptoken = opptokens[token]
    if (board, token) not in movesCache:
        movesCache[(board, token)] = findMoves(board, token, dP)
    futMoves = movesCache[(board, token)]
    if not futMoves:
        if (board, opptoken) not in movesCache:
            movesCache[(board, opptoken)] = findMoves(board, opptoken, dP)
        oppMoves = movesCache[(board, opptoken)]
        if not oppMoves: return [board.count(token) - board.count(opptoken)]
        ab = alphabeta(board, opptoken, -uprBnd, -lwrBnd, dP)
        return [-ab[0]] + ab[1:] + [-1]
    best = [lwrBnd-1]

    for move in futMoves:
        if move in cnrS:
            cnrMoves.append(move)
        else:
            goingMoves.append(move)
    cnrMoves.extend(goingMoves)

    moves = cnrMoves
    for move in moves:
        if (board, token, move) not in makerCache:
            makerCache[(board, token, move)] = makeMove(board, token, move, dP)
        changedBoard, newDot = makerCache[(board, token, move)]
        ab = alphabeta(changedBoard, opptoken, -uprBnd, -lwrBnd, newDot)
        score = -ab[0]
        if score < lwrBnd: continue
        if score > uprBnd: return [score]
        best = [score] + ab[1:] + [move]
        lwrBnd = score + 1
    return best

def alphabetaMain(board, token, lwrBnd, uprBnd, dP):
    cnrMoves = []
    goingMoves = []
    opptoken = opptokens[token]
    if (board, token) not in movesCache:
        movesCache[(board, token)] = findMoves(board, token, dP)
    futMoves = movesCache[(board, token)]
    if not futMoves:
        if (board, opptoken) not in movesCache:
            movesCache[(board, opptoken)] = findMoves(board, opptoken, dP)
        oppMoves = movesCache[(board, opptoken)]
        if not oppMoves: return [board.count(token) - board.count(opptoken)]
        ab = alphabeta(board, opptoken, -uprBnd, -lwrBnd, dP)
        return [-ab[0]] + ab[1:] + [-1]
    best = [lwrBnd-1]

    for move in futMoves:
        if move in cnrS:
            cnrMoves.append(move)
        else:
            goingMoves.append(move)
    cnrMoves.extend(goingMoves)

    moves = cnrMoves
    for mv in moves:
        if (board, token, mv) not in makerCache:
            makerCache[(board, token, mv)] = makeMove(board, token, mv, dP)
        changedBoard, newDot = makerCache[(board, token, mv)]
        ab = alphabeta(changedBoard, opptoken, -uprBnd, -lwrBnd, newDot)
        score = -ab[0]
        if score < lwrBnd: continue
        if score > uprBnd: return [score]
        best = [score] + ab[1:] + [mv]
        lwrBnd = score + 1
        print(f"Score: {score}; Sequence: {best[1:]}")
    return best

# midgame

def midgame(board, token, lwrBnd, uprBnd, lvl, dP):
    cnrMoves = []
    goingMoves = []
    opptoken = opptokens[token]
    if (board, token) not in movesCache:
        movesCache[(board, token)] = findMoves(board, token, dP)
    futMoves = movesCache[(board, token)]
    if not futMoves:
        if (board, opptoken) not in movesCache:
            movesCache[(board, opptoken)] = findMoves(board, opptoken, dP)
        oppMoves = movesCache[(board, opptoken)]
        if not oppMoves:
            return [heuristic(board, token, len(futMoves), len(oppMoves), 0, 0, 0, 0)]
        ab = midgame(board, opptoken, -uprBnd, -lwrBnd, lvl+1, dP)
        return [-ab[0]] + ab[1:] + [-1]

    if lvl > 5:
        if (board, opptoken) not in movesCache:
            movesCache[(board, opptoken)] = findMoves(board, opptoken, dP)
        oppMoves = movesCache[(board, opptoken)]
        return [heuristic(board, token, len(futMoves), len(oppMoves), 0, 0, 0, 0)]

    for move in futMoves:
        if move in cnrS:
            cnrMoves.append(move)
        else:
            goingMoves.append(move)
    cnrMoves.extend(goingMoves)

    moves = cnrMoves
    best = [lwrBnd-1]
    for mv in moves:
        if (board, token, mv) not in makerCache:
            makerCache[(board, token, mv)] = makeMove(board, token, mv, dP)
        changedBoard, newDot = makerCache[(board, token, mv)]
        ab = midgame(changedBoard, opptoken, -uprBnd, -lwrBnd, lvl+1, newDot)
        score = -ab[0]
        if score < lwrBnd: continue
        if score > uprBnd: return [score]
        best = [score] + ab[1:] + [mv]
        lwrBnd = score + 1
        if lvl == 1:
            print(f"Score: {score}; Sequence: {best[1:]}")
    return best



def heuristic(board, token, currMove, oppMove, scoreCnr, scoreFill, normScore, varScore):
    oppTok = opptokens[token]
    for corner in cnrS:
        if board[corner] == token:
            scoreCnr += 1
        if board[corner] == oppTok:
            scoreCnr -= 1
    for ind in cnrNeigh:
        if board[ind] == token:
            if board[cnrNeigh[ind]] == ".": scoreFill -= 1
        if board[ind] == oppTok:
            if board[cnrNeigh[ind]] == ".": scoreFill += 1
    if currMove < oppMove: varScore = -(100 * oppMove) / (currMove + oppMove)
    elif currMove > oppMove: varScore = (100*currMove) / (currMove+oppMove)
    return  int(382*scoreFill+ 800*scoreCnr + 120*normScore + 78.9*varScore)

if __name__ == "__main__":
    main()

# Medha Pappula, 6, 2026