import sys; args = sys.argv[1:]
import time

N,subblock_height,subblock_width,symbol_set,indToBox, boxToInd=0,0,0,set(),dict(),dict()

def make_constraints(board):
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

    indToBox={}
    boxToInd={}
    box=-1
    for x in range(height*width):
        if x%height!=0:
            box-=height
        for y in range(height*width):
            ind=x*height*width+y
            if y%width==0:
                box+=1
            indToBox[ind]=box
            lis=boxToInd.get(box,[])
            boxToInd[box]=lis+[ind]
    return N, height, width, symbol_set,indToBox,boxToInd

def is_valid(state,ind,symbol):
    row=ind//N
    col=ind%N
    box=indToBox[ind]
    for r in range(N):
        indy=r*N+col
        if state[indy]==symbol:
            return False
        indl=row*N+r
        if state[indl]==symbol:
            return False
    for index in boxToInd[box]:
        if state[index]==symbol:
            return False
    return True

def get_sorted_values(state,ind):
    return [item for item in symbol_set if is_valid(state,ind,item)]

def get_next_unassigned_variable(state,possible):
    minNum=10
    minInd=-1
    for index in range(N ** 2):
        if 0<len(possible[index])<minNum:
            minNum=len(possible[index])
            minInd=index
    return minInd

def update(mdict,index,symbol):
    ones=set()
    mdict[index]=""
    box=indToBox[index]
    for ind in boxToInd[box]:
        a=mdict[ind]
        if symbol in a:
            a=a.replace(symbol,"")
            if len(a)==1:
                ones.add(ind)
            if len(a)==0:
                return None,None
            mdict[ind]=a
    row=index//N
    for ind in range(N*row,N*(row+1)):
        a = mdict[ind]
        if symbol in a:
            a = a.replace(symbol, "")
            if len(a) == 1:
                ones.add(ind)
            if len(a) == 0:
                return None, None
            mdict[ind] = a
    col=index%N
    for ind in range(col,N*(N)+col,N):
        a = mdict[ind]
        if symbol in a:
            a = a.replace(symbol, "")
            if len(a) == 1:
                ones.add(ind)
            if len(a) == 0:
                return None, None
            mdict[ind] = a
    return mdict,ones


def populate(board):
    dict={}
    ones=set()
    options=[]
    ones=set()
    for index in range(len(board)):
        ad=""
        if board[index]==".":
            ad="".join([symbol for symbol in symbol_set if is_valid(board,index,symbol)])
            if len(ad)==1:
                ones.add(index)
            if len(ad)==0:
                return None,index
        options.append(ad)
    return options,ones

def constraint_propagation(dict,state):
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
    return dict,state

def forward_looking(state):
    if state is None:
        return None,None
    if "." not in state:
        return {},state
    dict,ones=populate(state)
    if dict is None:
        return None,None
    if len(ones)==0:
        return dict,state
    new_state=state
    while len(ones)>0:
        index=ones.pop()
        new_state = new_state[:index] + dict[index] + new_state[index + 1:]
    if not check(new_state):
        return None,None
    new_dict,new_state=constraint_propagation(dict,new_state)
    return forward_looking(new_state)

def csp_backtracking2(state,dict):
    if "." not in state:
        return state
    index=get_next_unassigned_variable(state,dict)
    for symbol in dict[index]:
        new_state = state[:index] + symbol + state[index + 1:]
        new_dict,new_state= forward_looking(new_state)
        if new_state is not None:
            result=csp_backtracking2(new_state,new_dict)
            if result is not None:
                return result
    return None


def crude_check(board):
    if board is None:
        return False
    counts=set()
    for item in symbol_set:
        counts.add(board.count(item))
    return len(counts)==1

def check(board):
    for box in range(N):
        myset=set()
        count=0
        for i in boxToInd[box]:
            if board[i]==".":
                count+=1
            else:
                myset.add(board[i])
        if len(myset)+count<N:
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
        for i in range(col, N **2 + col, N):
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
        
        N, subblock_height, subblock_width, symbol_set, indToBox, boxToInd = make_constraints(board)
        if check(board):
            dict,tmp=forward_looking(board)
            solution = csp_backtracking2(tmp, dict)
            
        print(f"{count}: {board}")
        spaces = " "*len(str(count) + ": ")
        print(f"{spaces}{solution} 324 {round(time.time() - startTime, 2)}s")
        count += 1

# Medha Pappula, 6, 2026