n = 4
tiles = list(range(1, n+1))

board = "abcde..hijklmnop"
CHARS = "abcdabcdabcdabcd"
possibleTiles = CHARS[:(n*n)]

def isValid(board):

    for i in range(0, len(board), n):
        tmp = [*board[i:i+n]]
        if sorted(list(set(tmp))) != sorted(tmp):
            return False

    for i in range(n):
        tmp = []
        for x in range(n):
            tmp.append(board[i+(x*n)])
        if sorted(list(set(tmp))) != sorted(tmp):
            return False
    
    tmp = []
    tmp2 = []

    for i in range(n):
        tmp.append(board[i+(i*n)])
        tmp2.append(board[i+(n*(n-1-i))])
    
    if sorted(list(set(tmp))) != sorted(tmp):
        return False

    if sorted(list(set(tmp2))) != sorted(tmp2):
        return False

    return True

def isSolved(board):
    return "." not in board

def choices(board):
    ind = board.index(".")
    tmp = {*possibleTiles}

    for c in board[(ind//n)*n:(ind//n+1)*n]:
        if c != ".":
            tmp.discard(c)
    
    for i in range(n):
        if board[ind//n+(i*n)] != ".":
            tmp.discard(board[ind//n+(i*n)])

    if ind//n == ind-((ind//n)*n):
        for i in range(n):
            if board[i+(i*n)] != ".":
                tmp.discard(board[i+(i*n)])
    
    if ind//n + ind-((ind//n)*n) == n-1:
        for i in range(n):
            if board[i+(n*(n-1-i))] != ".":
                tmp.discard(board[i+(n*(n-1-i))])

    ret = set()
    for c in tmp:
        ret.add(board[:ind] + c + board[ind+1:])
    
    return ret

def bruteForce(board):
    if not isValid(board):
        return ""
    if isSolved(board):
        return board
    
    chs = choices(board)

    for choice in chs:
        bF = bruteForce(choice)
        print(bF)
        if bF != "":
            return bF
    
    return ""

b = bruteForce(board)

for i in range(0, len(b), n):
    print(b[i:i+n]) 
