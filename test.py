board = "........."
size = 3
ln = 9

GAMES = 0
LINES = [[0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [2, 4, 6]]

visitedBoards = []

def solved(board):
    for line in LINES:
        l = "".join([board[x] for x in line])
        if l == "x"*3 or l == "o"*3:
            return True
    return False

def possMoves(board):
    return [x for x in range(9) if board[x] == "."]

def makeMove(board, tkn, move):
    return board[:move] + tkn + board[move+1:] 
    
def printBoard(board):
    print()
    for i in range(0, 9, 3):
        print(board[i:i+3])
    print()

def searchBoards(board, tkn, oppTkn):
    global GAMES, visitedBoards
    if board not in visitedBoards:
        visitedBoards.append(board)
    
        if (solved(board) or board.count(".") == 0):
            GAMES += 1
            return 1
        else:
            sum = 0
            for move in possMoves(board):
                sum += searchBoards(makeMove(board, tkn, move), oppTkn, tkn)
            return sum
    return 0


print("Total Number Of Games:", searchBoards(board, "x", "o")) #including starting board
print("Total Number Of Games(Backup):", GAMES)

print("Total Number Of Boards:", len(visitedBoards))

#255 168