n = int(input("Puzzle Size?: "))
tiles = list(range(1, n+1))

board = "."*(n*n)
nums = list(range(1,n+1))
TILES = [str(n) for i in range(n) for n in nums]


def isValid(board):
    return True
    """
    if "." in board:

    for row in range(n):
        tmp = [board[i] for i in range(row*n, row*n + n)]
        if collections.Counter(tmp) != collections.Counter(list(set(tmp))):
            return False
    
    for i in range(col, n*n, n):
        if board[i] == change:
            return False
    
    if row == col:
        for i in range(n):
            if board[i*n + i] == change:
                return False
    
    if row + col == n-1:
        for i in range(n):
            if board[(n-i)*n + i] == change:
                return False
            
    """


def isSolved(board):
    if "." in board:
        return False
    
    return True

def validMove(board, change):
    pos = board.index(".")
    row = pos//n
    col = pos - (pos//n)*n

    for i in range(row*n, row*n + n):
        if board[i] == change:
            return False
    
    for i in range(col, n*n, n):
        if board[i] == change:
            return False
    
    if row == col:
        for i in range(n):
            if board[i*n + i] == change:
                return False
    
    if row + col == n-1:
        for i in range(n):
            if board[(n-i-1)*n + i] == change:
                return False
    
    return True

def choices(board):
    retTiles = TILES.copy()
    for b in board:
        if b != ".":
            retTiles.remove(b)
    
    retSet = set()
    pos = board.index(".")

    for t in set(retTiles):
        if validMove(board, t):
            retSet.add(board[0:pos]+t+board[pos+1:])

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

for i in range(n):
    print(b[i*n:i*n+n])