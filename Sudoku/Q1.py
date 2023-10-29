n = 4
tiles = list(range(1, n+1))

board = "abcde..hijklmnop"
CHARS = "abcdefghijklmnop"
possibleTiles = CHARS[:(n*n)]

def isValid(board):
    print("------------------> CHECK ZERO PASSED")
    for i in range(0, len(board), n):
        tmp = [*board[i:i+n]]
        if sorted(list(set(tmp))) != sorted(tmp):
            return False
    print("------------------> CHECK ONE PASSED")
    for i in range(n):
        tmp = []
        for x in range(n):
            tmp.append(board[i+(x*n)])
        if sorted(list(set(tmp))) != sorted(tmp):
            return False
    print("------------------> CHECK TWO PASSED")
    tmp = []
    tmp2 = []

    for i in range(n):
        tmp.append(board[i+(i*n)])
        tmp2.append(board[i+(n*(n-1-i))])
    print("------------------> CHECK THREE PASSED")
    if sorted(list(set(tmp))) != sorted(tmp):
        return False
    print("------------------> CHECK FOUR PASSED")
    if sorted(list(set(tmp2))) != sorted(tmp2):
        return False
    print("------------------> CHECK FIVE PASSED")
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
    print("valid")
    if isSolved(board):
        return board
    print("not solved")

    chs = choices(board)
    print("choices made")

    for choice in chs:
        print(choice)
        bF = bruteForce(choice)
        print(bF)
        if bF != "":
            return bF
    
    return ""

b = bruteForce(board)

for i in range(0, len(b), n):
    print(b[i:i+n]) 
