import sys; args = sys.argv[1:]
import time

puzzles = open(args[0]).read().split("\n")
    
def isValid(state, ind, symbol):
    row = ind // N
    col = ind % N
    box = indToBox[ind]
    for r in range(N):
        indy = r * N + col
        if state[indy] == symbol:
            return False
        indl = row * N + r
        if state[indl] == symbol:
            return False
    for index in boxToInd[box]:
        if state[index] == symbol:
            return False
    return True

def setGlobals(board):
    N = int(len(board) ** .5)
    symbols = "123456789ABCDEFGHIJKLMNOPQRSTUVQXYZ"
    symbols = symbols[:N]
    symbol_set = set(symbols)
    if "." in symbol_set:
        symbol_set.remove(".")
    height = -1
    i = int(N ** .5)
    while i < N and height == -1:
        if N % i == 0:
            height = i
        i += 1
    width = N // height

    indToBox = {}  # {0:0,1:0,2:1}
    boxToInd = {}  # {0:[0,1],1:[2,3]}
    box = -1
    for x in range(height * width):
        if x % height != 0:
            box -= height
        for y in range(height * width):
            ind = x * height * width + y
            if y % width == 0:
                box += 1
            indToBox[ind] = box
            lis = boxToInd.get(box, [])
            boxToInd[box] = lis + [ind]
    return N, height, width, symbol_set, indToBox, boxToInd

def checkSum(puzzle):
    min_ascii = min(ord(char) for char in puzzle)
    checksum = 0
    for char in puzzle:
        checksum += ord(char) - min_ascii
    return checksum

def bruteForce(puzzle):
    def solve(board):
        for ind, symbol in enumerate(board):
            if symbol == '.':
                for s in symbol_set:
                    if isValid(board, ind, s):
                        board[ind] = s
                        if solve(board):
                            return True
                        board[ind] = '.'
                return False
        return True

    setGlobals(puzzle)
    board = list(puzzle)
    if solve(board):
        return ''.join(board)
    else:
        return "No solution"

count = 1

for board in puzzles:
    N, subHeight, subWidth, symbol_set, indToBox, boxToInd = setGlobals(board)
    
    startTime = time.time()
    solution = bruteForce(board)
    print(str(count) + ": " + board)
    print((" "*(len(str(count) + ": "))) + str(solution) + " " + str("324") + " " + str(round(time.time()-startTime, 2)) + "s")
    #checksum = checkSum(solution)
    #print("Checksum:", checksum)
    count = count + 1


# Medha Pappula, 6, 2026