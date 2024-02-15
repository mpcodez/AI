STRTBRD = '.'*27 + 'ox......xo' + '.'*27
NBRFLIPS = {}
NBRMOVES = {}
SUBSETS = []
TKNLOCS = {}

def setup(args):
    global STRTBRD, NBRFLIPS, NBRMOVES, SUBSETS, TKNLOCS

    STRTBRD = args[0].lower()
    TKNLOCS = {'o': {i for i in range(64) if STRTBRD[i] == 'o'} - {0, 7, 56, 63}, 'x': {i for i in range(64) if STRTBRD[i] == 'x'} - {0, 7, 56, 63}}

    allIndeces = list(range(0, len(STRTBRD)))

    for index in allIndeces:
        if index % 8 == 7:
            NBRFLIPS[index] = {index - 1, index - 8, index + 7, index - 9, index + 8}.intersection(allIndeces)
        elif index % 8 == 0:
            NBRFLIPS[index] = {index - 8, index + 9, index - 7, index + 8, index + 1}.intersection(allIndeces)
        else:
            NBRFLIPS[index] = {index - 1, index + 8, index + 7, index + 9, index - 8, index - 7, index - 9, index + 1}.intersection(allIndeces)

    for index in allIndeces:

        subDict = {neighbor: [] for neighbor in NBRFLIPS[index]}

        for neighbor in NBRFLIPS[index]:
            p = neighbor
            randVAl = index - neighbor
            current = neighbor + randVAl
            count = 0

            while -1 < current < 64 and current in NBRFLIPS[p]:
                if current != index:
                    count += 1
                    subDict[neighbor].append(current)
                p = current
                current = current + randVAl

            if count == 0:
               del subDict[neighbor]
            
        SUBSETS.append(subDict)

    NBRMOVES = {index: k for index in NBRFLIPS if len(k:={key for key in SUBSETS[index]}) != 0}

def getNext(board):
    return "o", "x" if board.count('.') % 2 else "x", "o"

def getOpposite(currToken):
    return "o" if currToken == "x" else "x"

def indexWorks(board, currToken, adjInd, possInd):
    subset = SUBSETS[adjInd][possInd]

    for index in subset:
        if board[index] == currToken: return True
        elif board[index] == '.': return False
     
    return False

def getOpposite(currToken):
    return "o" if currToken == "x" else "x"

def getNextMoves(board, currToken):
    global NBRMOVES
    possibleMoves = set()

    for idx in TKNLOCS[getOpposite(currToken)]:
        for neighbor in NBRMOVES[idx]:
            if board[neighbor] == '.' and indexWorks(board, currToken, idx, neighbor):
                possibleMoves.add(neighbor)
    
    return possibleMoves

def choose_move(board, player, still_running, time_limit):
    setup([board, player])
    possMoves = getNextMoves(board, player)
    return list(possMoves)[0]

class Strategy:
    def best_strategy(self, board, player, best_move, still_running, time_limit):
        move = choose_move(board, player, still_running, time_limit)
        best_move.value = move