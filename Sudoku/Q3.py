board = " ..... .............. ..... "

hexagons = [{14, 15, 16, 17, 18, 19, 20}, {7, 8, 9, 10, 11, 12, 13}, {22, 23, 24, 25, 26}, {1, 2, 3, 4, 5}, {25, 26, 19, 20, 13}, {23, 24, 17, 18, 11, 12, 5}, {3, 4, 9, 10, 15, 16, 22}, {1, 2, 7, 8, 14}, {4, 5, 12, 13, 20}, {2, 3, 10, 11, 18, 19, 26}, {1, 8, 9, 16, 17, 24, 25}, {7, 14, 15, 22, 23}, {9, 10, 11, 16, 17, 18}, {1, 2, 3, 8, 9, 10}, {3, 4, 5, 10, 11, 12}, {7, 8, 9, 14, 15, 16}, {11, 12, 13, 18, 19, 20}, {15, 16, 17, 22, 23, 24}, {7, 8, 9, 24, 25, 26}]

TILES = {"1", "2", "3", "4", "5", "6", "7"}

def isSolved(board):
    return "." not in board

def choices(board):
    retTiles = set(TILES.copy())

    if "." in board[9:12]:
        pos = (board[9:12]).index(".") + 9
    elif "." in board[16:19]:
        pos = (board[16:19]).index(".") + 16
    else:
        pos = board.index(".")
    
    for h in hexagons:
        if pos in h:
            for tri in h:
                retTiles.discard(board[tri])

    retSet = set()

    for r in retTiles:
        retSet.add(board[:pos] + r + board[pos+1:])

    return retSet


def bruteForce(board):
    
    if isSolved(board):
        return board

    chs = choices(board)

    for choice in chs:
        bF = bruteForce(choice)
        if bF != "":
            return bF
    
    return ""

b = bruteForce(board)

for x in range(0, len(board), 7):
    print(" ".join(b[x:x+7]))