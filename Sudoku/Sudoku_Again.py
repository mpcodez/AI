import sys; args = sys.argv[1:]
import time

N = 9
subblock_height = 3
subblock_width = 3
symbol_set = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
indToBox = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 0, 10: 0, 11: 0, 12: 1, 13: 1, 14: 1, 15: 2, 16: 2, 17: 2, 18: 0, 19: 0, 20: 0, 21: 1, 22: 1, 23: 1, 24: 2, 25: 2, 26: 2, 27: 3, 28: 3, 29: 3, 30: 4, 31: 4, 32: 4, 33: 5, 34: 5, 35: 5, 36: 3, 37: 3, 38: 3, 39: 4, 40: 4, 41: 4, 42: 5, 43: 5, 44: 5, 45: 3, 46: 3, 47: 3, 48: 4, 49: 4, 50: 4, 51: 5, 52: 5, 53: 5, 54: 6, 55: 6, 56: 6, 57: 7, 58: 7, 59: 7, 60: 8, 61: 8, 62: 8, 63: 6, 64: 6, 65: 6, 66: 7, 67: 7, 68: 7, 69: 8, 70: 8, 71: 8, 72: 6, 73: 6, 74: 6, 75: 7, 76: 7, 77: 7, 78: 8, 79: 8, 80: 8}
boxToInd = {0: [0, 1, 2, 9, 10, 11, 18, 19, 20], 1: [3, 4, 5, 12, 13, 14, 21, 22, 23], 2: [6, 7, 8, 15, 16, 17, 24, 25, 26], 3: [27, 28, 29, 36, 37, 38, 45, 46, 47], 4: [30, 31, 32, 39, 40, 41, 48, 49, 50], 5: [33, 34, 35, 42, 43, 44, 51, 52, 53], 6: [54, 55, 56, 63, 64, 65, 72, 73, 74], 7: [57, 58, 59, 66, 67, 68, 75, 76, 77], 8: [60, 61, 62, 69, 70, 71, 78, 79, 80]}
constraints = {0: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 27, 36, 45, 54, 63, 72}, 1: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 28, 37, 46, 55, 64, 73}, 2: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 29, 38, 47, 56, 65, 74}, 3: {0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 30, 39, 48, 57, 66, 75}, 4: {0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 31, 40, 49, 58, 67, 76}, 5: {0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 32, 41, 50, 59, 68, 77}, 6: {0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 24, 25, 26, 33, 42, 51, 60, 69, 78}, 7: {0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 24, 25, 26, 34, 43, 52, 61, 70, 79}, 8: {0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 24, 25, 26, 35, 44, 53, 62, 71, 80}, 9: {0, 1, 2, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 27, 36, 45, 54, 63, 72}, 10: {0, 1, 2, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 28, 37, 46, 55, 64, 73}, 11: {0, 1, 2, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 29, 38, 47, 56, 65, 74}, 12: {3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 30, 39, 48, 57, 66, 75}, 13: {3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 31, 40, 49, 58, 67, 76}, 14: {3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 32, 41, 50, 59, 68, 77}, 15: {6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 24, 25, 26, 33, 42, 51, 60, 69, 78}, 16: {6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 24, 25, 26, 34, 43, 52, 61, 70, 79}, 17: {6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 24, 25, 26, 35, 44, 53, 62, 71, 80}, 18: {0, 1, 2, 9, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 36, 45, 54, 63, 72}, 19: {0, 1, 2, 9, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 37, 46, 55, 64, 73}, 20: {0, 1, 2, 9, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 29, 38, 47, 56, 65, 74}, 21: {3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 30, 39, 48, 57, 66, 75}, 22: {3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 31, 40, 49, 58, 67, 76}, 23: {3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 32, 41, 50, 59, 68, 77}, 24: {6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 33, 42, 51, 60, 69, 78}, 25: {6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 34, 43, 52, 61, 70, 79}, 26: {6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 35, 44, 53, 62, 71, 80}, 27: {0, 9, 18, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 54, 63, 72}, 28: {1, 10, 19, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 55, 64, 73}, 29: {2, 11, 20, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 56, 65, 74}, 30: {3, 12, 21, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 57, 66, 75}, 31: {4, 13, 22, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 58, 67, 76}, 32: {5, 14, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 59, 68, 77}, 33: {6, 15, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42, 43, 44, 51, 52, 53, 60, 69, 78}, 34: {7, 16, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42, 43, 44, 51, 52, 53, 61, 70, 79}, 35: {8, 17, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42, 43, 44, 51, 52, 53, 62, 71, 80}, 36: {0, 9, 18, 27, 28, 29, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 54, 63, 72}, 37: {1, 10, 19, 27, 28, 29, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 55, 64, 73}, 38: {2, 11, 20, 27, 28, 29, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 56, 65, 74}, 39: {3, 12, 21, 30, 31, 32, 36, 37, 38, 39, 40, 41, 42, 43, 44, 48, 49, 50, 57, 66, 75}, 40: {4, 13, 22, 30, 31, 32, 36, 37, 38, 39, 40, 41, 42, 43, 44, 48, 49, 50, 58, 67, 76}, 41: {5, 14, 23, 30, 31, 32, 36, 37, 38, 39, 40, 41, 42, 43, 44, 48, 49, 50, 59, 68, 77}, 42: {6, 15, 24, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 51, 52, 53, 60, 69, 78}, 43: {7, 16, 25, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 51, 52, 53, 61, 70, 79}, 44: {8, 17, 26, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 51, 52, 53, 62, 71, 80}, 45: {0, 9, 18, 27, 28, 29, 36, 37, 38, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 63, 72}, 46: {1, 10, 19, 27, 28, 29, 36, 37, 38, 45, 46, 47, 48, 49, 50, 51, 52, 53, 55, 64, 73}, 47: {2, 11, 20, 27, 28, 29, 36, 37, 38, 45, 46,47, 48, 49, 50, 51, 52, 53, 56, 65, 74}, 48: {3, 12, 21, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 49, 50, 51, 52, 53, 57, 66, 75}, 49: {4, 13, 22, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 49, 50, 51, 52, 53, 58, 67, 76}, 50: {5, 14, 23, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 49, 50, 51, 52, 53, 59, 68, 77}, 51: {6, 15, 24, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 60, 69, 78}, 52: {7, 16, 25, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 61, 70, 79}, 53: {8, 17, 26, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 62, 71, 80}, 54: {0, 9, 18, 27, 36, 45, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74}, 55: {1, 10, 19, 28, 37, 46, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74}, 56: {2, 11, 20, 29, 38, 47, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74}, 57: {3, 12, 21, 30, 39, 48, 54, 55, 56, 57, 58, 59, 60, 61, 62, 66, 67, 68, 75, 76, 77}, 58: {4, 13, 22, 31, 40, 49, 54, 55, 56, 57, 58, 59, 60, 61, 62, 66, 67, 68, 75, 76, 77}, 59: {5, 14, 23, 32, 41, 50, 54, 55, 56, 57, 58, 59, 60, 61, 62, 66, 67, 68, 75, 76, 77}, 60: {6, 15, 24, 33, 42, 51, 54, 55, 56, 57, 58, 59, 60, 61, 62, 69, 70, 71, 78, 79, 80}, 61: {7, 16, 25, 34, 43, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 69, 70, 71, 78, 79, 80}, 62: {8, 17, 26, 35, 44, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 69, 70, 71, 78, 79, 80}, 63: {0, 9, 18, 27, 36, 45, 54, 55, 56, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74}, 64: {1, 10, 19, 28, 37, 46, 54, 55, 56, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74}, 65: {2, 11, 20, 29, 38, 47, 54, 55, 56, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74}, 66: {3, 12, 21, 30, 39, 48, 57, 58, 59, 63, 64, 65, 66, 67, 68, 69, 70, 71, 75, 76, 77}, 67: {4, 13, 22, 31, 40, 49, 57, 58, 59, 63, 64, 65, 66, 67, 68, 69, 70, 71, 75, 76, 77}, 68: {5, 14, 23, 32, 41, 50, 57, 58, 59, 63, 64, 65, 66, 67, 68, 69, 70, 71, 75, 76, 77}, 69: {6, 15, 24, 33, 42, 51, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 78, 79, 80}, 70: {7, 16, 25, 34, 43, 52, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 78, 79, 80}, 71: {8, 17, 26, 35, 44, 53, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 78, 79, 80}, 72: {0, 9, 18, 27, 36, 45, 54, 55, 56, 63, 64, 65, 72, 73, 74, 75, 76, 77, 78, 79, 80}, 73: {1, 10, 19, 28, 37, 46, 54, 55, 56, 63, 64, 65, 72, 73, 74, 75, 76, 77, 78, 79, 80}, 74: {2, 11, 20, 29, 38, 47, 54, 55, 56, 63, 64, 65, 72, 73, 74, 75, 76, 77, 78, 79, 80}, 75: {3, 12, 21, 30, 39, 48, 57, 58, 59, 66, 67, 68, 72, 73, 74, 75, 76, 77, 78, 79, 80}, 76: {4, 13, 22, 31, 40, 49, 57, 58, 59, 66, 67, 68, 72, 73, 74, 75, 76, 77, 78, 79, 80}, 77: {5, 14, 23, 32, 41, 50, 57, 58, 59, 66, 67, 68, 72, 73, 74, 75, 76, 77, 78, 79, 80}, 78: {6, 15, 24, 33, 42, 51, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80}, 79: {7, 16, 25, 34, 43, 52, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80}, 80: {8, 17, 26, 35, 44, 53, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80}}

def is_valid(state, ind, symbol):
    for i in constraints[ind]:
        if state[i] == symbol:
            return False
        
    return True


def get_next_unassigned_variable(state, possible, ones):
    if len(ones) > 0:
        return ones.pop()
    minNum = 10
    minInd = -1
    for index in range(N ** 2):
        if 0 < len(possible[index]) < minNum:
            minNum = len(possible[index])
            minInd = index
    return minInd


def forward_look(state, mdict, index, symbol, ones):
    mdict[index] = ""
    box = indToBox[index]
    for ind in boxToInd[box]:
        # if ind!=index and state[ind]==".":
        a = mdict[ind]
        if symbol in a:
            a = a.replace(symbol, "")
            if len(a) == 1:
                ones.add(ind)
            if len(a) == 0:
                return None, None
            mdict[ind] = a
    row = index // N
    for ind in range(N * row, N * (row + 1)):
        a = mdict[ind]
        if symbol in a:
            a = a.replace(symbol, "")
            if len(a) == 1:
                ones.add(ind)
            if len(a) == 0:
                return None, None
            mdict[ind] = a
    col = index % N
    for ind in range(col, N * (N) + col, N):
        a = mdict[ind]
        if symbol in a:
            a = a.replace(symbol, "")
            if len(a) == 1:
                ones.add(ind)
            if len(a) == 0:
                return None, None
            mdict[ind] = a
    return mdict, ones


def populate(board):
    options = []
    ones = set()
    for index in range(len(board)):
        ad = ""
        if board[index] == ".":
            ad = "".join([symbol for symbol in symbol_set if is_valid(board, index, symbol)])
            if len(ad) == 1:
                ones.add(index)
        options.append(ad)
    return options, ones


def constraint_propagation(state, dictionary):
    for box in range(N):
        objects = [state[index] for index in boxToInd[box]]
        for symbol in symbol_set:
            if symbol not in objects:
                present = [symbol in dictionary[index] for index in boxToInd[box]]
                if present.count(True) == 0:
                    return None, None
                if present.count(True) == 1:
                    index = boxToInd[box][present.index(True)]
                    state = state[:index] + symbol + state[index + 1:]
                    dictionary[index] = ""
    for row in range(N):
        objects = [state[index] for index in range(N * row, N * (row + 1))]
        for symbol in symbol_set:
            if symbol not in objects:
                present=[symbol in dictionary[index] for index in range(N*row,N*row+N)]
                if present.count(True) == 0:
                    return None, None
                if present.count(True) == 1:
                    index = row*N+present.index(True)
                    state = state[:index] + symbol + state[index + 1:]
                    dictionary[index] = ""
    for col in range(N):
        for row in range(N):
            objects = [state[index] for index in range(col, N **2+col,N)]
            for symbol in symbol_set:
                if symbol not in objects:
                    present = [symbol in dictionary[index] for index in range(col, N **2+col,N)]
                    if present.count(True) == 0:
                        return None, None
                    if present.count(True) == 1:
                        index = col+N * present.index(True)
                        state = state[:index] + symbol + state[index + 1:]
                        dictionary[index] = ""
    return state,dictionary

def solve(state, dictionary, ones):
    if check(state) == False:
        return None
    if "." not in state:
        return state
    if len(ones)==0:
        state,dictionary=constraint_propagation(state,dictionary)
        if dictionary is None or check(state) == False:
            return None
        if "." not in state:
            return state
            
    index = get_next_unassigned_variable(state, dictionary, ones)
    for symbol in dictionary[index]:
        if is_valid(state, index, symbol):
            new_state = state[:index] + symbol + state[index + 1:]
            new_dict=dictionary.copy()
            new_dict[index]=""
            new_dict, new_ones = forward_look(state, new_dict, index, symbol, ones.copy())
            if new_dict is not None:
                result = solve(new_state, new_dict, new_ones)
                if result is not None:
                    return result
    
    return None

def check(board):
    for box in range(N):
        myset = set()
        count = 0
        for i in boxToInd[box]:
            if board[i] == ".":
                count += 1
            else:
                myset.add(board[i])
        if len(myset) + count < N:
            return False
    for row in range(N):
        myset = set()
        count = 0
        for i in range(N * row, N * (row + 1)):
            if board[i] == ".":
                count += 1
            else:
                myset.add(board[i])
        if len(myset) + count < N:
            return False
    for col in range(N):
        myset = set()
        count = 0
        for i in range(col, N ** 2 + col, N):
            if board[i] == ".":
                count += 1
            else:
                myset.add(board[i])
        if len(myset) + count < N:
            return False
    return True

if __name__ == "__main__":
    puzzles = open(args[0]).read().split("\n")

    count = 1

    for board in puzzles:
        
        startTime = time.time()
        
        dictionary, ones = populate(board)
        solution = solve(board, dictionary, ones)
        
        print(f"{count}: {board}")
        spaces = " "*len(str(count) + ": ")
        print(f"{spaces}{solution} 324 {round(time.time() - startTime, 2)}s")
        count += 1

# Medha Pappula, 6, 2026

"""
Again, but not again :(

def bruteForce():
- find list of choices by way of best dot
if no bail out (number of choices > 1)
    All sym in SYMSET:
        determine possible positions for each symbol in List Of Constraint Sets
        if possible positions for sym < lstOfChoices: #we have something better
            update LstOfChoices #use the symbol instead of a dot


Improvements:
    - Best Dot: dot that has the least possible options for symbols
    - Best Symbol: symbol that has the least amount of indicies(positions) as to where it could possibly be in a CONSTRAINT SET
    - Naked Pairs:
    - incrementeal programming
    - lookup tables
    - buckets

Naked Pairs:
    - find two cells in the same constraint set with same TWO (2) options
    - elimate both options from all other constraint sets

def bruteForce(puzzle):
    pos = findBestDot(puzzle)
    if possible symbols for that position doesn't have length 1:
        sym = findBestSymbol(puzzle)
        if Best symbols not 1:
            nakedPairs()


"""