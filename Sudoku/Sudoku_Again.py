import sys; args = sys.argv[1:]
import time

N = 9
subblock_height = 3
subblock_width = 3
symbol_set = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
indToBox = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 0, 10: 0, 11: 0, 12: 1, 13: 1, 14: 1, 15: 2, 16: 2, 17: 2, 18: 0, 19: 0, 20: 0, 21: 1, 22: 1, 23: 1, 24: 2, 25: 2, 26: 2, 27: 3, 28: 3, 29: 3, 30: 4, 31: 4, 32: 4, 33: 5, 34: 5, 35: 5, 36: 3, 37: 3, 38: 3, 39: 4, 40: 4, 41: 4, 42: 5, 43: 5, 44: 5, 45: 3, 46: 3, 47: 3, 48: 4, 49: 4, 50: 4, 51: 5, 52: 5, 53: 5, 54: 6, 55: 6, 56: 6, 57: 7, 58: 7, 59: 7, 60: 8, 61: 8, 62: 8, 63: 6, 64: 6, 65: 6, 66: 7, 67: 7, 68: 7, 69: 8, 70: 8, 71: 8, 72: 6, 73: 6, 74: 6, 75: 7, 76: 7, 77: 7, 78: 8, 79: 8, 80: 8}
boxToInd = {0: [0, 1, 2, 9, 10, 11, 18, 19, 20], 1: [3, 4, 5, 12, 13, 14, 21, 22, 23], 2: [6, 7, 8, 15, 16, 17, 24, 25, 26], 3: [27, 28, 29, 36, 37, 38, 45, 46, 47], 4: [30, 31, 32, 39, 40, 41, 48, 49, 50], 5: [33, 34, 35, 42, 43, 44, 51, 52, 53], 6: [54, 55, 56, 63, 64, 65, 72, 73, 74], 7: [57, 58, 59, 66, 67, 68, 75, 76, 77], 8: [60, 61, 62, 69, 70, 71, 78, 79, 80]}

def is_valid(state, ind, symbol):
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


def get_sorted_values(dictionary, ind):
    return dictionary[ind]


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


def constraint_propagation(state, dict):
    for box in range(N):
        objects = [state[index] for index in boxToInd[box]]
        for symbol in symbol_set:
            if symbol not in objects:
                present = [symbol in dict[index] for index in boxToInd[box]]
                if present.count(True) == 0:
                    return None, None
                if present.count(True) == 1:
                    index = boxToInd[box][present.index(True)]
                    state = state[:index] + symbol + state[index + 1:]
                    dict[index] = ""
    for row in range(N):
        objects = [state[index] for index in range(N * row, N * (row + 1))]
        for symbol in symbol_set:
            if symbol not in objects:
                present=[symbol in dict[index] for index in range(N*row,N*row+N)]
                if present.count(True) == 0:
                    return None, None
                if present.count(True) == 1:
                    index = row*N+present.index(True)
                    state = state[:index] + symbol + state[index + 1:]
                    dict[index] = ""
    for col in range(N):
        for row in range(N):
            objects = [state[index] for index in range(col, N **2+col,N)]
            for symbol in symbol_set:
                if symbol not in objects:
                    present = [symbol in dict[index] for index in range(col, N **2+col,N)]
                    if present.count(True) == 0:
                        return None, None
                    if present.count(True) == 1:
                        index = col+N * present.index(True)
                        state = state[:index] + symbol + state[index + 1:]
                        dict[index] = ""
    return state,dict

def solve(state, dict, ones):
    if "." not in state:
        return state
    if len(ones)==0:
        state,dict=constraint_propagation(state,dict)
        if dict is None:
            return None
        if "." not in state:
            return state
            
    index = get_next_unassigned_variable(state, dict, ones)
    for symbol in dict[index]:  # get_sorted_values(dict,index):
        new_state = state[:index] + symbol + state[index + 1:]
        new_dict=dict.copy()
        new_dict[index]=""
        new_dict, new_ones = forward_look(state, new_dict, index, symbol, ones.copy())
        if new_dict is not None:

            result = solve(new_state, new_dict, new_ones)
            if result is not None and ("." not in result and check(result)):
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
        
        if check(board):
            dict, ones = populate(board)
            solution = solve(board, dict, ones)
        
        print(f"{count}: {board}")
        spaces = " "*len(str(count) + ": ")
        print(f"{spaces}{solution} 324 {round(time.time() - startTime, 2)}s")
        count += 1

# Medha Pappula, 6, 2026